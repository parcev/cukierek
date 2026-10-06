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
    flag: "https://flagcdn.com/pl.svg", // Dostosuj ścieżkę do swojej flagi

    // HTML Static Content
    card_title: "🍬 Otrzymaj cukierek!",
    card_desc: "<span class='red'>Zaobserwuj</span> nasz profil, a następnie <span class='red'>wróć</span> tutaj i <span class='red'>odbierz cukierek</span> za każde media społecznościowe.",
    header_fb: "🔵 Facebook",
    header_ig: "📸 Instagram",

    // Buttons
    btn_fb_start: "1. Zaobserwuj nas na Facebooku",
    btn_fb_claimed: "✅ Facebook — cukierek odebrany",
    btn_fb_goto: "✅ Przejdź na Facebooka",
    btn_fb_verify: "2. Otrzymaj cukierek za zaobserwowanie na Facebooku",

    btn_ig_start: "1. Zaobserwuj nas na Instagramie",
    btn_ig_claimed: "✅ Instagram — cukierek odebrany",
    btn_ig_goto: "✅ Przejdź na Instagram",
    btn_ig_verify: "2. Otrzymaj cukierek za zaobserwowanie na Instagramie",

    // Status Messages & Errors
    status_prep_session: "⏳ Przygotowywanie sesji...",
    status_session_expired: "⌛ Sesja wygasła. Możesz rozpocząć nową.",
    status_fb_click_verify: "Kliknij przycisk \"Otrzymaj cukierek za Facebook\"",
    status_ig_click_verify: "👆 Kliknij przycisk \"Otrzymaj cukierek za Instagram\"",
    status_checking_fb: "🔎 Sprawdzam Facebook...",
    status_checking_ig: "🔎 Sprawdzam Instagram...",
    status_success_fb: "🎉 Facebook zweryfikowany! Zabierz cukierka z podajnika.",
    status_success_ig: "🎉 Instagram zweryfikowany! Zabierz cukierka z podajnika.",
    status_not_verified_fb: "❌ Nie wykryto jeszcze nowego obserwującego na Facebooku. Upewnij się, że zaobserwowałeś stronę i spróbuj ponownie.",
    status_not_verified_ig: "❌ Nie wykryto jeszcze nowego obserwującego na Instagramie. Upewnij się, że zaobserwowałeś profil i spróbuj ponownie.",
    status_claimed_both: "🍬 Odebrałeś już oba cukierki.",
    status_fb_claimed: "🍬 Cukierek Facebook został już odebrany.",
    status_ig_claimed: "🍬 Cukierek Instagram został już odebrany.",
    status_busy: "⏳ Automat jest obecnie zajęty. Spróbuj ponownie za chwilę.",
    status_error: "⚠️ Wystąpił błąd.",
    session_active: "⏱️ Sesja aktywna"
  },

  lt: {
    label: "LT",
    flag: "https://flagcdn.com/lt.svg", // Dostosuj ścieżkę do swojej flagi

    // HTML Static Content
    card_title: "🍬 Gaukite saldainį!",
    card_desc: "<span class='red'>Sekite</span> mūsų profilį, tuomet <span class='red'>grįžkite</span> čia ir <span class='red'>pasiimkite saldainį</span> už kiekvieną socialinį tinklą.",
    header_fb: "🔵 Facebook",
    header_ig: "📸 Instagram",

    // Buttons
    btn_fb_start: "1. Sekite mus Facebooke",
    btn_fb_claimed: "✅ Facebook — saldainis atsiimtas",
    btn_fb_goto: "✅ Eiti į Facebook",
    btn_fb_verify: "2. Gaukite saldainį už Facebook sekimą",

    btn_ig_start: "1. Sekite mus Instagram",
    btn_ig_claimed: "✅ Instagram — saldainis atsiimtas",
    btn_ig_goto: "✅ Eiti į Instagram",
    btn_ig_verify: "2. Gaukite saldainį už Instagram sekimą",

    // Status Messages & Errors
    status_prep_session: "⏳ Ruošiama sesija...",
    status_session_expired: "⌛ Sesija pasibaigė. Galite pradėti naują.",
    status_fb_click_verify: "Spustelėkite mygtuką \"Gaukite saldainį už Facebook\"",
    status_ig_click_verify: "👆 Spustelėkite mygtuką \"Gaukite saldainį už Instagram\"",
    status_checking_fb: "🔎 Tikrinamas Facebook...",
    status_checking_ig: "🔎 Tikrinamas Instagram...",
    status_success_fb: "🎉 Facebook patvirtintas! Pasiimkite saldainį.",
    status_success_ig: "🎉 Instagram patvirtintas! Pasiimkite saldainį.",
    status_not_verified_fb: "❌ Naujas Facebook sekėjas dar nepastebėtas. Įsitikinkite, kad užsiprenumeravote puslapį, ir bandykite dar kartą.",
    status_not_verified_ig: "❌ Naujas Instagram sekėjas dar nepastebėtas. Įsitikinkite, kad užsiprenumeravote profilį, ir bandykite dar kartą.",
    status_claimed_both: "🍬 Jau atsiėmėte abu saldainius.",
    status_fb_claimed: "🍬 Facebook saldainis jau atsiimtas.",
    status_ig_claimed: "🍬 Instagram saldainis jau atsiimtas.",
    status_busy: "⏳ Aparatas šiuo metu užimtas. Bandykite dar kartą po akimirkos.",
    status_error: "⚠️ Įvyko klaida.",
    session_active: "⏱️ Aktyvi sesija"
  },

  en: {
    label: "EN",
    flag: "https://flagcdn.com/en.svg", // Dostosuj ścieżkę do swojej flagi

    // HTML Static Content
    card_title: "🍬 Get a candy!",
    card_desc: "<span class='red'>Follow</span> our profile, then <span class='red'>return</span> here and <span class='red'>claim your candy</span> for each social platform.",
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
    status_session_expired: "⌛ Session expired. You can start a new one.",
    status_fb_click_verify: "Click \"Get candy for Facebook\"",
    status_ig_click_verify: "👆 Click \"Get candy for Instagram\"",
    status_checking_fb: "🔎 Checking Facebook...",
    status_checking_ig: "🔎 Checking Instagram...",
    status_success_fb: "🎉 Facebook verified! Grab your candy.",
    status_success_ig: "🎉 Instagram verified! Grab your candy.",
    status_not_verified_fb: "❌ New Facebook follower not detected yet. Make sure you followed the page and try again.",
    status_not_verified_ig: "❌ New Instagram follower not detected yet. Make sure you followed the profile and try again.",
    status_claimed_both: "🍬 You have already claimed both candies.",
    status_fb_claimed: "🍬 Facebook candy already claimed.",
    status_ig_claimed: "🍬 Instagram candy already claimed.",
    status_busy: "⏳ Machine is currently busy. Try again in a moment.",
    status_error: "⚠️ An error occurred.",
    session_active: "⏱️ Active session"
  }
};

/*
==================================================
POMOCNIKI TŁUMACZEŃ
==================================================
*/

// Pobieranie tekstu tłumaczenia na podstawie klucza
function t(key) {
  return (translations[ currentLang ] && translations[ currentLang ][ key ]) || translations[ DEFAULT_LANG ][ key ] || key;
}

// Główna funkcja zmiany języka
function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("user_lang", lang);

  // 1. Aktualizacja flagi i napisu w wybranym języku na przycisku rozwijanym
  const langData = translations[ lang ] || translations[ DEFAULT_LANG ];
  const selectedLangEl = document.getElementById("selected-lang");
  const selectedFlagEl = document.getElementById("selected-flag");

  if (selectedLangEl) selectedLangEl.innerText = langData.label;
  if (selectedFlagEl) selectedFlagEl.src = langData.flag;

  // 2. Automatyczne tłumaczenie elementów z data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (translations[ lang ] && translations[ lang ][ key ]) {
      el.innerHTML = translations[ lang ][ key ];
    }
  });

  // 3. Re-render dynamicznych elementów strony
  if (typeof updateButtons === "function") updateButtons();
  if (typeof updateSessionInfo === "function") updateSessionInfo();
}

/*
==================================================
OBSŁUGA MENU DROPDOWN
==================================================
*/

function toggleLangDropdown(event) {
  event.stopPropagation();
  const menu = document.getElementById("langMenu");
  if (menu) menu.classList.toggle("show");
}

function selectLang(langCode) {
  const menu = document.getElementById("langMenu");
  if (menu) menu.classList.remove("show");

  if (typeof setLanguage === 'function') {
    setLanguage(langCode);
  }
}

// Zamknięcie menu po kliknięciu poza nim
window.addEventListener('click', () => {
  const menu = document.getElementById("langMenu");
  if (menu) menu.classList.remove("show");
});

// Inicjalizacja języka po załadowaniu drzewa DOM
document.addEventListener("DOMContentLoaded", () => {
  setLanguage(currentLang);
});