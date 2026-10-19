/*
==================================================
KONFIGURACJA I SŁOWNIK
==================================================
*/

const DEFAULT_LANG = "pl";
let currentLang = localStorage.getItem("user_lang") || DEFAULT_LANG;

const translations = {
  pl: {
    label: "PL",
    flag: "https://flagcdn.com/pl.svg",

    
 // HTML Static Content
    card_title: "🍬 Odbierz cukierka!",
    card_desc:
      "<span class='red'>Zaobserwuj</span> nasz profil, a następnie <span class='red'>wróć</span> tutaj i <span class='red'>odbierz cukierka</span> za każde medium społecznościowe.",
    header_fb: "🔵 Facebook",
    header_ig: "📸 Instagram",

    // Buttons
    btn_fb_start: "1. Zaobserwuj nas na Facebooku",
    btn_fb_claimed: "✅ Facebook — cukierek odebrany",
    btn_fb_goto: "✅ Otwórz Facebook",
    btn_fb_verify: "2. Odbierz cukierka za obserwowanie na Facebooku",

    btn_ig_start: "1. Zaobserwuj nas na Instagramie",
    btn_ig_claimed: "✅ Instagram — cukierek odebrany",
    btn_ig_goto: "✅ Otwórz Instagram",
    btn_ig_verify: "2. Odbierz cukierka za obserwowanie na Instagramie",

    // Status Messages & Errors
    status_prep_session: "⏳ Przygotowujemy sesję...",
    status_session_expired: "⌛ Sesja wygasła. Rozpocznij nową.",

    status_fb_click_verify:
      "👆 Kliknij „Odbierz cukierka za Facebooka”.",
    status_ig_click_verify:
      "👆 Kliknij „Odbierz cukierka za Instagram”.",

    status_checking_fb: "🔎 Sprawdzamy Facebooka...",
    status_checking_ig: "🔎 Sprawdzamy Instagrama...",

    status_success_fb:
      "🎉 Facebook zweryfikowany! Odbierz cukierka z automatu.",
    status_success_ig:
      "🎉 Instagram zweryfikowany! Odbierz cukierka z automatu.",

    status_not_verified_fb:
      "❌ Nie wykryliśmy jeszcze nowego obserwującego na Facebooku. Upewnij się, że obserwujesz naszą stronę, i spróbuj ponownie.",
    status_not_verified_ig:
      "❌ Nie wykryliśmy jeszcze nowego obserwującego na Instagramie. Upewnij się, że obserwujesz nasz profil, i spróbuj ponownie.",

    status_claimed_both: "🍬 Odebrałeś już oba cukierki.",
    status_fb_claimed: "🍬 Cukierek za Facebooka został już odebrany.",
    status_ig_claimed: "🍬 Cukierek za Instagram został już odebrany.",

    status_fb_claimed_can_ig:
      "✅ Cukierek za Facebooka odebrany. Możesz też odebrać cukierka za Instagram.",
    status_ig_claimed_can_fb:
      "✅ Cukierek za Instagram odebrany. Możesz też odebrać cukierka za Facebooka.",

    status_popup_blocked_fb:
      "⚠️ Przeglądarka zablokowała otwarcie Facebooka. Zezwól na wyskakujące okna i spróbuj ponownie.",
    status_popup_blocked_ig:
      "⚠️ Przeglądarka zablokowała otwarcie Instagrama. Zezwól na wyskakujące okna i spróbuj ponownie.",

    status_no_connection: "⚠️ Brak połączenia z serwerem.",
    status_busy:
      "⏳ Automat jest zajęty. Spróbuj ponownie za chwilę.",
    status_error: "⚠️ Coś poszło nie tak.",
    session_active: "⏱️ Sesja aktywna"

  },

  lt: {
    label: "LT",
    flag: "https://flagcdn.com/lt.svg",

    // HTML Static Content
card_title: "🍬 Gaukite saldainį!",
card_desc:
  "<span class='red'>Stebėkite</span> mus „Facebook“ arba <span class='red'>sekite</span> „Instagram“, tada <span class='red'>grįžkite</span> čia ir <span class='red'>atsiimkite saldainį</span> už kiekvieną socialinį tinklą.",
header_fb: "🔵 Facebook",
header_ig: "📸 Instagram",

// Buttons
btn_fb_start: "1. Stebėkite mus „Facebook“",
btn_fb_claimed: "✅ „Facebook“ saldainis atsiimtas",
btn_fb_goto: "✅ Atidaryti „Facebook“",
btn_fb_verify: "2. Atsiimti saldainį už stebėjimą „Facebook“",

btn_ig_start: "1. Sekite mus „Instagram“",
btn_ig_claimed: "✅ „Instagram“ saldainis atsiimtas",
btn_ig_goto: "✅ Atidaryti „Instagram“",
btn_ig_verify: "2. Atsiimti saldainį už sekimą „Instagram“",

// Status Messages & Errors
status_prep_session: "⏳ Ruošiama sesija...",
status_session_expired:
  "⌛ Sesija baigėsi. Galite pradėti iš naujo.",

status_fb_click_verify:
  "👆 Spustelėkite mygtuką „Atsiimti saldainį už stebėjimą „Facebook““.",
status_ig_click_verify:
  "👆 Spustelėkite mygtuką „Atsiimti saldainį už sekimą „Instagram““.",

status_checking_fb: "🔎 Tikrinama, ar stebite „Facebook“ puslapį...",
status_checking_ig: "🔎 Tikrinama, ar sekate „Instagram“ profilį...",

status_success_fb:
  "🎉 „Facebook“ stebėjimas patvirtintas! Atsiimkite savo saldainį.",
status_success_ig:
  "🎉 „Instagram“ sekimas patvirtintas! Atsiimkite savo saldainį.",

status_not_verified_fb:
  "❌ Nepavyko patvirtinti, kad stebite mūsų „Facebook“ puslapį. Įsitikinkite, kad jį stebite, ir bandykite dar kartą.",
status_not_verified_ig:
  "❌ Nepavyko patvirtinti, kad sekate mūsų „Instagram“ profilį. Įsitikinkite, kad jį sekate, ir bandykite dar kartą.",

status_claimed_both: "🍬 Jau atsiėmėte abu saldainius!",
status_fb_claimed: "🍬 Saldainis už „Facebook“ puslapio stebėjimą jau atsiimtas.",
status_ig_claimed: "🍬 Saldainis už „Instagram“ profilio sekimą jau atsiimtas.",

status_fb_claimed_can_ig:
  "✅ Saldainį už „Facebook“ puslapio stebėjimą jau atsiėmėte. Taip pat galite atsiimti saldainį už „Instagram“ profilio sekimą.",
status_ig_claimed_can_fb:
  "✅ Saldainį už „Instagram“ profilio sekimą jau atsiėmėte. Taip pat galite atsiimti saldainį už „Facebook“ puslapio stebėjimą.",

status_popup_blocked_fb:
  "⚠️ Naršyklė užblokavo „Facebook“ langą. Leiskite atidaryti iššokančiuosius langus ir bandykite dar kartą.",
status_popup_blocked_ig:
  "⚠️ Naršyklė užblokavo „Instagram“ langą. Leiskite atidaryti iššokančiuosius langus ir bandykite dar kartą.",

status_no_connection: "⚠️ Nepavyksta susisiekti su serveriu. Patikrinkite interneto ryšį.",
status_busy:
  "⏳ Saldainių aparatas šiuo metu užimtas. Pabandykite dar kartą po akimirkos.",
status_error: "⚠️ Įvyko klaida. Bandykite dar kartą.",
session_active: "⏱️ Sesija aktyvi"
  },

  en: {
    label: "EN",
    flag: "https://flagcdn.com/gb.svg",

    // HTML Static Content
    card_title: "🍬 Get a candy!",
    card_desc:
      "<span class='red'>Follow</span> our profile, then <span class='red'>return</span> here and <span class='red'>claim your candy</span> for each social platform.",
    header_fb: "🔵 Facebook",
    header_ig: "📸 Instagram",

    // Buttons
    btn_fb_start: "1. Follow us on Facebook",
    btn_fb_claimed: "✅ Facebook — candy claimed",
    btn_fb_goto: "✅ Go to Facebook",
    btn_fb_verify: "2. Get candy for Facebook follow",

    btn_ig_start: "1. Follow us on Instagram",
    btn_ig_claimed: "✅ Instagram — candy claimed",
    btn_ig_goto: "✅ Go to Instagram",
    btn_ig_verify: "2. Get candy for Instagram follow",

    // Status Messages & Errors
    status_prep_session: "⏳ Preparing session...",
    status_session_expired:
      "⌛ Session expired. You can start a new one.",

    status_fb_click_verify:
      "👆 Click the „Get candy for Facebook” button.",
    status_ig_click_verify:
      "👆 Click the „Get candy for Instagram” button.",

    status_checking_fb: "🔎 Checking Facebook...",
    status_checking_ig: "🔎 Checking Instagram...",

    status_success_fb:
      "🎉 Facebook verified! Grab your candy.",
    status_success_ig:
      "🎉 Instagram verified! Grab your candy.",

    status_not_verified_fb:
      "❌ New Facebook follower not detected yet. Make sure you followed the page and try again.",
    status_not_verified_ig:
      "❌ New Instagram follower not detected yet. Make sure you followed the profile and try again.",

    status_claimed_both:
      "🍬 You have already claimed both candies.",
    status_fb_claimed:
      "🍬 Facebook candy already claimed.",
    status_ig_claimed:
      "🍬 Instagram candy already claimed.",

    status_fb_claimed_can_ig:
      "✅ Facebook claimed. You can also claim candy for Instagram.",
    status_ig_claimed_can_fb:
      "✅ Instagram claimed. You can also claim candy for Facebook.",

    status_popup_blocked_fb:
      "⚠️ Browser blocked Facebook. Allow popups and try again.",
    status_popup_blocked_ig:
      "⚠️ Browser blocked Instagram. Allow popups and try again.",

    status_no_connection:
      "⚠️ No connection to the server.",
    status_busy:
      "⏳ Machine is currently busy. Try again in a moment.",
    status_error:
      "⚠️ An error occurred.",
    session_active:
      "⏱️ Active session"
  }
};


/*
==================================================
POMOCNIKI TŁUMACZEŃ
==================================================
*/

// Pobieranie tłumaczenia na podstawie klucza
function t(key) {
  return (
    (translations[ currentLang ] && translations[ currentLang ][ key ]) ||
    translations[ DEFAULT_LANG ][ key ] ||
    key
  );
}


// Główna funkcja zmiany języka
function setLanguage(lang) {
  // Jeżeli podany język nie istnieje, użyj domyślnego
  if (!translations[ lang ]) {
    lang = DEFAULT_LANG;
  }

  currentLang = lang;
  localStorage.setItem("user_lang", lang);

  // Aktualizacja wybranego języka
  const langData = translations[ lang ];

  const selectedLangEl = document.getElementById("selected-lang");
  const selectedFlagEl = document.getElementById("selected-flag");

  if (selectedLangEl) {
    selectedLangEl.innerText = langData.label;
  }

  if (selectedFlagEl) {
    selectedFlagEl.src = langData.flag;
  }

  // Tłumaczenie elementów statycznych
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");

    if (langData[ key ]) {
      el.innerHTML = langData[ key ];
    }
  });

  // Aktualizacja dynamicznych elementów
  if (typeof updateButtons === "function") {
    updateButtons();
  }

  if (typeof updateSessionInfo === "function") {
    updateSessionInfo();
  }

  // Ponowne wyświetlenie aktualnego statusu
  if (typeof renderStatus === "function") {
    renderStatus();
  }
}


/*
==================================================
OBSŁUGA MENU JĘZYKOWEGO
==================================================
*/

function toggleLangDropdown(event) {
  event.stopPropagation();

  const menu = document.getElementById("langMenu");

  if (menu) {
    menu.classList.toggle("show");
  }
}


function selectLang(langCode) {
  const menu = document.getElementById("langMenu");

  if (menu) {
    menu.classList.remove("show");
  }

  setLanguage(langCode);
}


// Zamknięcie menu po kliknięciu poza nim
window.addEventListener("click", () => {
  const menu = document.getElementById("langMenu");

  if (menu) {
    menu.classList.remove("show");
  }
});


/*
==================================================
INICJALIZACJA
==================================================
*/

document.addEventListener("DOMContentLoaded", () => {
  setLanguage(currentLang);
});
