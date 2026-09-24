import os
import time
import secrets
import threading

import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# CONFIG

SESSION_DURATION = 8 * 60

MAX_ACTIVE_SESSIONS = 3

FOLLOWER_CHECKS = 5
FOLLOWER_CHECK_INTERVAL = 2

DISPENSE_COOLDOWN = 5


# META GRAPH API

# Wersja API jest ustawiona bezpośrednio w kodzie.
META_API_VERSION = "v24.0"


# ENVIRONMENT VARIABLES

# FACEBOOK

FB_PAGE_ID = os.getenv("FB_PAGE_ID")

# Page Access Token.
# Ten sam token jest używany przez
# Facebook oraz Instagram API with Facebook Login.

FB_ACCESS_TOKEN = os.getenv(
    "FB_ACCESS_TOKEN"
)


# INSTAGRAM

# ID konta Instagram Professional
# połączonego ze stroną Facebook.

IG_USER_ID = os.getenv(
    "IG_USER_ID"
)


# ADAFRUIT

ADAFRUIT_USERNAME = os.getenv(
    "ADAFRUIT_USERNAME"
)

ADAFRUIT_KEY = os.getenv(
    "ADAFRUIT_KEY"
)


# ADMIN

ADMIN_KEY = os.getenv(
    "ADMIN_KEY",
    "super-secret-admin-key"
)


# DISCORD - OPTIONAL

DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)


# FRONTEND

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "*"
)


# CHECK ENVIRONMENT

required_vars = {
    "FB_PAGE_ID": FB_PAGE_ID,
    "FB_ACCESS_TOKEN": FB_ACCESS_TOKEN,
    "IG_USER_ID": IG_USER_ID,
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


# APP

app = FastAPI(
    title="Candy Dispenser API"
)


# CORS

origins = []

if FRONTEND_ORIGIN and FRONTEND_ORIGIN != "*":
    origins = [FRONTEND_ORIGIN]

app.add_middleware(
    CORSMiddleware,

    allow_origins=(
        origins
        if origins
        else ["*"]
    ),

    allow_credentials=False,

    allow_methods=[
        "GET",
        "POST"
    ],

    allow_headers=[
        "Content-Type",
        "X-Admin-Key"
    ],
)


# MEMORY

sessions = {}

state_lock = threading.Lock()

last_dispense_time = 0


# MODELS

class StartSessionRequest(BaseModel):
    platform: str


class StartSessionResponse(BaseModel):
    session_id: str
    expires_in: int


class StartPlatformRequest(BaseModel):
    session_id: str
    platform: str


class VerifyRequest(BaseModel):
    session_id: str
    platform: str


class ManualDispenseRequest(BaseModel):
    admin_key: str


# SESSION HELPERS

def is_valid_platform(platform):
    return platform in [
        "facebook",
        "instagram"
    ]


def cleanup_sessions():

    now = time.time()

    expired = []

    with state_lock:

        for session_id, data in sessions.items():

            if data["expires_at"] <= now:
                expired.append(session_id)

        for session_id in expired:
            del sessions[session_id]


def get_session(session_id):

    session = sessions.get(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="SESSION_EXPIRED"
        )

    if session["expires_at"] <= time.time():

        sessions.pop(
            session_id,
            None
        )

        raise HTTPException(
            status_code=410,
            detail="SESSION_EXPIRED"
        )

    return session


# FACEBOOK FOLLOWERS

def get_facebook_follower_count():

    if not FB_PAGE_ID:
        raise RuntimeError(
            "FB_PAGE_ID is not configured"
        )

    if not FB_ACCESS_TOKEN:
        raise RuntimeError(
            "FB_ACCESS_TOKEN is not configured"
        )

    url = (
        "https://graph.facebook.com/"
        f"{META_API_VERSION}/"
        f"{FB_PAGE_ID}"
    )

    params = {
        "fields": "followers_count",
        "access_token": FB_ACCESS_TOKEN
    }

    response = requests.get(
        url,
        params=params,
        timeout=5
    )

    if not response.ok:

        try:
            error_data = response.json()

        except Exception:
            error_data = {
                "raw": response.text
            }

        raise RuntimeError(
            "Facebook Meta API error: "
            f"{error_data}"
        )

    data = response.json()

    count = data.get(
        "followers_count"
    )

    if count is None:
        raise RuntimeError(
            "Facebook Meta API did not "
            "return followers_count"
        )

    return int(count)


# INSTAGRAM FOLLOWERS
#
# Instagram API with Facebook Login.
#
# Używamy tego samego Page Access Tokena,
# który jest używany dla strony Facebook.

def get_instagram_follower_count():

    if not IG_USER_ID:
        raise RuntimeError(
            "IG_USER_ID is not configured"
        )

    if not FB_ACCESS_TOKEN:
        raise RuntimeError(
            "FB_ACCESS_TOKEN is not configured"
        )

    url = (
        "https://graph.facebook.com/"
        f"{META_API_VERSION}/"
        f"{IG_USER_ID}"
    )

    params = {
        "fields": "followers_count",
        "access_token": FB_ACCESS_TOKEN
    }

    response = requests.get(
        url,
        params=params,
        timeout=5
    )

    if not response.ok:

        try:
            error_data = response.json()

        except Exception:
            error_data = {
                "raw": response.text
            }

        raise RuntimeError(
            "Instagram Meta API error: "
            f"{error_data}"
        )

    data = response.json()

    count = data.get(
        "followers_count"
    )

    if count is None:
        raise RuntimeError(
            "Instagram Meta API did not "
            "return followers_count"
        )

    return int(count)


# GENERIC FOLLOWER COUNT

def get_follower_count(platform):

    if platform == "facebook":
        return get_facebook_follower_count()

    if platform == "instagram":
        return get_instagram_follower_count()

    raise ValueError(
        "Unsupported platform"
    )


# ADAFRUIT

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
        "https://io.adafruit.com/api/v2/"
        f"{ADAFRUIT_USERNAME}/feeds/"
        "cukierki/data"
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


# DISCORD

def send_discord(
    dispense_id,
    platform=None,
    manual=False
):

    if not DISCORD_WEBHOOK_URL:
        return

    tag = (
        "🔴 **[MANUAL]**"
        if manual
        else "🍬"
    )

    platform_text = ""

    if platform:
        platform_text = (
            f"\nPlatforma: `{platform}`"
        )

    payload = {
        "content": (
            f"{tag} **Cukierko-Bot:** "
            "wysłano polecenie "
            "wydania cukierka."
            f"{platform_text}\n"
            f"ID: `{dispense_id}`"
        )
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


# ROOT

@app.get("/")
def root():

    return {
        "status": "online",
        "system": "Candy Dispenser Backend"
    }


# START SESSION

@app.post(
    "/api/start-session",
    response_model=StartSessionResponse
)
def start_session(
    req: StartSessionRequest
):
  
    
    if not is_valid_platform(req.platform):

        raise HTTPException(
            status_code=400,
            detail="INVALID_PLATFORM"
        )

    cleanup_sessions()

    with state_lock:

        if len(sessions) >= MAX_ACTIVE_SESSIONS:

            raise HTTPException(
                status_code=429,
                detail="FULL"
            )

        # Pobierz początkową liczbę Facebook

        try:

            facebook_initial = (
                get_facebook_follower_count()
            )

        except Exception as error:

            raise HTTPException(
                status_code=502,
                detail=(
                    "Nie można pobrać "
                    "stanu Facebook: "
                    f"{error}"
                )
            )

        # Pobierz początkową liczbę Instagram

        try:

            instagram_initial = (
                get_instagram_follower_count()
            )

        except Exception as error:

            raise HTTPException(
                status_code=502,
                detail=(
                    "Nie można pobrać "
                    "stanu Instagram: "
                    f"{error}"
                )
            )

        session_id = (
            secrets.token_urlsafe(32)
        )

        now = time.time()

        sessions[session_id] = {

            "created_at":
                now,

            "expires_at":
                now + SESSION_DURATION,

            # Które platformy użytkownik rozpoczął

            "facebook_started":
                req.platform == "facebook",

            "instagram_started":
                req.platform == "instagram",

            # Facebook

            "facebook_initial":
                facebook_initial,

            "facebook_dispensed":
                False,

            # Instagram

            "instagram_initial":
                instagram_initial,

            "instagram_dispensed":
                False
        }

    return {
        "session_id":
            session_id,

        "expires_in":
            SESSION_DURATION
    }


# START SECOND PLATFORM IN EXISTING SESSION

@app.post(
    "/api/start-platform"
)
def start_platform(
    req: StartPlatformRequest
):

    if not is_valid_platform(req.platform):

        raise HTTPException(
            status_code=400,
            detail="INVALID_PLATFORM"
        )

    cleanup_sessions()

    with state_lock:

        session = get_session(
            req.session_id
        )

        started_key = (
            f"{req.platform}_started"
        )

        dispensed_key = (
            f"{req.platform}_dispensed"
        )

        if session[dispensed_key]:

            raise HTTPException(
                status_code=409,
                detail="ALREADY_USED"
            )

        session[started_key] = True

        return {
            "status": "success",
            "platform": req.platform,
            "expires_at":
                session["expires_at"],
            "facebook_started":
                session["facebook_started"],
            "instagram_started":
                session["instagram_started"],
            "facebook_dispensed":
                session["facebook_dispensed"],
            "instagram_dispensed":
                session["instagram_dispensed"]
        }


# GET SESSION STATE

@app.get(
    "/api/session/{session_id}"
)
def session_status(
    session_id: str
):

    cleanup_sessions()

    with state_lock:

        session = get_session(
            session_id
        )

        return {
            "status": "active",

            "expires_at":
                session["expires_at"],

            "facebook_started":
                session["facebook_started"],

            "instagram_started":
                session["instagram_started"],

            "facebook_dispensed":
                session["facebook_dispensed"],

            "instagram_dispensed":
                session["instagram_dispensed"]
        }


# VERIFY

@app.post(
    "/api/verify"
)
def verify(
    req: VerifyRequest
):

    if not is_valid_platform(req.platform):

        raise HTTPException(
            status_code=400,
            detail="INVALID_PLATFORM"
        )

    cleanup_sessions()

    # Pobranie sesji

    with state_lock:

        session = get_session(
            req.session_id
        )

        started_key = (
            f"{req.platform}_started"
        )

        dispensed_key = (
            f"{req.platform}_dispensed"
        )

        initial_key = (
            f"{req.platform}_initial"
        )

        # Platforma musi być wcześniej rozpoczęta

        if not session[started_key]:

            raise HTTPException(
                status_code=409,
                detail="PLATFORM_NOT_STARTED"
            )

        # Nie można odebrać drugi raz

        if session[dispensed_key]:

            raise HTTPException(
                status_code=409,
                detail="ALREADY_USED"
            )

        initial_count = (
            session[initial_key]
        )

    # Sprawdzanie followersów

    current_count = initial_count

    for attempt in range(
        FOLLOWER_CHECKS
    ):

        try:

            current_count = (
                get_follower_count(
                    req.platform
                )
            )

        except Exception as error:

            raise HTTPException(
                status_code=502,
                detail=(
                    "Błąd sprawdzania "
                    f"{req.platform}: "
                    f"{error}"
                )
            )

        if current_count > initial_count:
            break

        if attempt < FOLLOWER_CHECKS - 1:

            time.sleep(
                FOLLOWER_CHECK_INTERVAL
            )

    # Nie zweryfikowano

    if current_count <= initial_count:

        return {
            "status":
                "not_verified",

            "platform":
                req.platform,

            "initial_count":
                initial_count,

            "current_count":
                current_count
        }

    # Cooldown

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

        session = get_session(
            req.session_id
        )

        dispensed_key = (
            f"{req.platform}_dispensed"
        )

        if session[dispensed_key]:

            raise HTTPException(
                status_code=409,
                detail="ALREADY_USED"
            )

        dispense_id = (
            secrets.token_urlsafe(24)
        )

        session[dispensed_key] = True

        session[
            f"{req.platform}_dispense_id"
        ] = dispense_id

        last_dispense_time = now

    # Wyślij do Adafruit

    try:

        send_to_adafruit(
            dispense_id
        )

    except Exception as error:

        with state_lock:

            session = sessions.get(
                req.session_id
            )

            if session:

                session[
                    f"{req.platform}_dispensed"
                ] = False

                session.pop(
                    f"{req.platform}_dispense_id",
                    None
                )

        raise HTTPException(
            status_code=502,
            detail=(
                "Błąd Adafruit IO: "
                f"{error}"
            )
        )

    # Discord

    send_discord(
        dispense_id,
        platform=req.platform
    )

    # Usuń sesję dopiero wtedy,
    # gdy oba cukierki zostały odebrane.

    with state_lock:

        session = sessions.get(
            req.session_id
        )

        if session:

            both_done = (
                session["facebook_dispensed"]
                and
                session["instagram_dispensed"]
            )

            if both_done:

                sessions.pop(
                    req.session_id,
                    None
                )

    return {
        "status":
            "success",

        "platform":
            req.platform,

        "message":
            "Polecenie wydania wysłane."
    }


# MANUAL DISPENSE

@app.post(
    "/api/admin/manual-dispense"
)
def manual_dispense(
    req: ManualDispenseRequest
):

    if req.admin_key != ADMIN_KEY:

        raise HTTPException(
            status_code=401,
            detail="UNAUTHORIZED"
        )

    dispense_id = (
        "MANUAL_"
        + secrets.token_urlsafe(16)
    )

    try:

        send_to_adafruit(
            dispense_id
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=(
                "Błąd Adafruit IO: "
                f"{error}"
            )
        )

    send_discord(
        dispense_id,
        manual=True
    )

    return {
        "status":
            "success",

        "message":
            "Manualny sygnał został "
            "pomyślnie wysłany do "
            "Adafruit IO.",

        "dispense_id":
            dispense_id
    }