import os
import time
import secrets
import threading

import requests

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# =========================================================
# CONFIG
# =========================================================

SESSION_DURATION = 10 * 60

MAX_ACTIVE_SESSIONS = 3

FOLLOWER_CHECKS = 5
FOLLOWER_CHECK_INTERVAL = 2

DISPENSE_COOLDOWN = 5


# =========================================================
# ENVIRONMENT
# =========================================================

META_PAGE_ID = os.getenv("FB_PAGE_ID")
META_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

ADAFRUIT_USERNAME = os.getenv("ADAFRUIT_USERNAME")
ADAFRUIT_KEY = os.getenv("ADAFRUIT_KEY")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "*"
)


# =========================================================
# VALIDATION
# =========================================================

required_vars = {
    "FB_PAGE_ID": META_PAGE_ID,
    "FB_ACCESS_TOKEN": META_ACCESS_TOKEN,
    "ADAFRUIT_USERNAME": ADAFRUIT_USERNAME,
    "ADAFRUIT_KEY": ADAFRUIT_KEY,
}

missing = [
    name
    for name, value in required_vars.items()
    if not value
]

if missing:

    print(
        "WARNING: Missing environment variables:",
        ", ".join(missing)
    )


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Candy Dispenser API"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_origin_middleware(request: Request, call_next):
    origin = request.headers.get("origin") or request.headers.get("referer") or "Direct/Unknown"
    print(f"Incoming request to {request.url.path} from website: {origin}")
    response = await call_next(request)
    return response
# =========================================================
# MEMORY STATE
# =========================================================

sessions = {}

state_lock = threading.Lock()

last_dispense_time = 0


# =========================================================
# MODELS
# =========================================================

class StartSessionResponse(BaseModel):

    session_id: str

    expires_in: int


class VerifyRequest(BaseModel):

    session_id: str


# =========================================================
# HELPERS
# =========================================================

def cleanup_sessions():

    now = time.time()

    expired = []

    with state_lock:

        for session_id, data in sessions.items():

            if data["expires_at"] <= now:
                expired.append(session_id)

        for session_id in expired:
            del sessions[session_id]


def get_follower_count():

    if not META_PAGE_ID:
        raise RuntimeError(
            "FB_PAGE_ID is not configured"
        )

    if not META_ACCESS_TOKEN:
        raise RuntimeError(
            "FB_ACCESS_TOKEN is not configured"
        )

    url = (
        f"https://graph.facebook.com/"
        f"{META_PAGE_ID}"
    )

    params = {
        "fields": "followers_count",
        "access_token": META_ACCESS_TOKEN
    }

    response = requests.get(
        url,
        params=params,
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    count = data.get("followers_count")

    if count is None:
        raise RuntimeError(
            "Meta API did not return followers_count"
        )

    return int(count)


def send_to_adafruit(dispense_id):

    if not ADAFRUIT_USERNAME:
        raise RuntimeError(
            "ADAFRUIT_USERNAME is not configured"
        )

    if not ADAFRUIT_KEY:
        raise RuntimeError(
            "ADAFRUIT_KEY is not configured"
        )

    url = (
        f"https://io.adafruit.com/api/v2/"
        f"{ADAFRUIT_USERNAME}/feeds/"
        f"cukierki/data"
    )

    headers = {
        "X-AIO-Key": ADAFRUIT_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "value": f"DROP:{dispense_id}"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=5
    )

    response.raise_for_status()


def send_discord(dispense_id):

    if not DISCORD_WEBHOOK_URL:
        return

    payload = {
        "content":
            "🍬 **Cukierko-Bot:** "
            "wysłano polecenie wydania cukierka."
            f"\nID: `{dispense_id}`"
    }

    try:

        requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=3
        )

    except Exception as error:

        print(
            "Discord error:",
            error
        )


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "system": "Candy Dispenser Backend"
    }


# =========================================================
# START SESSION
# =========================================================

@app.post(
    "/api/start-session",
    response_model=StartSessionResponse
)
def start_session():

    cleanup_sessions()

    with state_lock:

        if len(sessions) >= MAX_ACTIVE_SESSIONS:

            raise HTTPException(
                status_code=429,
                detail="FULL"
            )

        try:

            initial_count = get_follower_count()

        except Exception as error:

            raise HTTPException(
                status_code=502,
                detail=(
                    "Nie można sprawdzić "
                    f"Facebook followers_count: {error}"
                )
            )

        session_id = secrets.token_urlsafe(32)

        sessions[session_id] = {
            "initial_count": initial_count,
            "created_at": time.time(),
            "expires_at":
                time.time() + SESSION_DURATION,
            "verified": False,
            "dispensed": False
        }

    return {
        "session_id": session_id,
        "expires_in": SESSION_DURATION
    }


# =========================================================
# VERIFY
# =========================================================

@app.post("/api/verify")
def verify(req: VerifyRequest):

    cleanup_sessions()

    with state_lock:

        session = sessions.get(
            req.session_id
        )

        if not session:

            raise HTTPException(
                status_code=404,
                detail="SESSION_EXPIRED"
            )

        if session["expires_at"] < time.time():

            del sessions[req.session_id]

            raise HTTPException(
                status_code=410,
                detail="SESSION_EXPIRED"
            )

        if session["dispensed"]:

            raise HTTPException(
                status_code=409,
                detail="ALREADY_USED"
            )

        initial_count = session[
            "initial_count"
        ]

    # -----------------------------------------------------
    # Sprawdzamy kilka razy.
    # -----------------------------------------------------

    current_count = initial_count

    for attempt in range(FOLLOWER_CHECKS):

        try:

            current_count = get_follower_count()

        except Exception as error:

            raise HTTPException(
                status_code=502,
                detail=(
                    "Błąd sprawdzania "
                    f"Facebook: {error}"
                )
            )

        if current_count > initial_count:
            break

        if attempt < FOLLOWER_CHECKS - 1:

            time.sleep(
                FOLLOWER_CHECK_INTERVAL
            )

    # -----------------------------------------------------
    # Brak wzrostu.
    # -----------------------------------------------------

    if current_count <= initial_count:

        return {
            "status": "not_verified",
            "initial_count": initial_count,
            "current_count": current_count
        }

    # -----------------------------------------------------
    # Dodatkowy globalny cooldown.
    # -----------------------------------------------------

    global last_dispense_time

    now = time.time()

    with state_lock:

        if (
            now - last_dispense_time
            < DISPENSE_COOLDOWN
        ):

            raise HTTPException(
                status_code=429,
                detail="TRY_AGAIN"
            )

        session = sessions.get(
            req.session_id
        )

        if not session:

            raise HTTPException(
                status_code=404,
                detail="SESSION_EXPIRED"
            )

        if session["dispensed"]:

            raise HTTPException(
                status_code=409,
                detail="ALREADY_USED"
            )

        dispense_id = secrets.token_urlsafe(24)

        session["verified"] = True
        session["dispensed"] = True
        session["dispense_id"] = dispense_id

        last_dispense_time = now

    # -----------------------------------------------------
    # Wyślij polecenie do Adafruit IO.
    # -----------------------------------------------------

    try:

        send_to_adafruit(
            dispense_id
        )

    except Exception as error:

        # Jeżeli Adafruit się nie udał,
        # cofamy stan sesji.

        with state_lock:

            session = sessions.get(
                req.session_id
            )

            if session:
                session["verified"] = False
                session["dispensed"] = False
                session.pop(
                    "dispense_id",
                    None
                )

        raise HTTPException(
            status_code=502,
            detail=(
                "Błąd Adafruit IO: "
                f"{error}"
            )
        )

    # -----------------------------------------------------
    # Discord
    # -----------------------------------------------------

    send_discord(
        dispense_id
    )

    # -----------------------------------------------------
    # Sesja zakończona.
    # -----------------------------------------------------

    with state_lock:

        sessions.pop(
            req.session_id,
            None
        )

    return {
        "status": "success",
        "message": "Polecenie wydania wysłane."
    }