"""
Multi-Language Support for Mindframe Platform
Internationalization (i18n) for Nordic and European markets
"""
from enum import Enum
from typing import Dict, Optional


class Language(str, Enum):
    """Supported languages"""
    EN_US = "en_US"  # English (United States)
    EN_GB = "en_GB"  # English (United Kingdom)
    NO_NB = "no_NB"  # Norwegian Bokmål
    NO_NN = "no_NN"  # Norwegian Nynorsk
    SV_SE = "sv_SE"  # Swedish
    DA_DK = "da_DK"  # Danish
    FI_FI = "fi_FI"  # Finnish
    DE_DE = "de_DE"  # German


# ============================================================================
# TRANSLATION DICTIONARIES
# ============================================================================

TRANSLATIONS = {
    # ========================================================================
    # COMMON / NAVIGATION
    # ========================================================================
    "nav.dashboard": {
        Language.EN_US: "Dashboard",
        Language.EN_GB: "Dashboard",
        Language.NO_NB: "Dashbord",
        Language.NO_NN: "Dashbord",
        Language.SV_SE: "Instrumentpanel",
        Language.DA_DK: "Dashboard",
        Language.FI_FI: "Kojelauta",
        Language.DE_DE: "Dashboard",
    },
    "nav.agents": {
        Language.EN_US: "AI Agents",
        Language.EN_GB: "AI Agents",
        Language.NO_NB: "AI-agenter",
        Language.NO_NN: "AI-agentar",
        Language.SV_SE: "AI-agenter",
        Language.DA_DK: "AI-agenter",
        Language.FI_FI: "AI-agentit",
        Language.DE_DE: "KI-Agenten",
    },
    "nav.marketplace": {
        Language.EN_US: "Marketplace",
        Language.EN_GB: "Marketplace",
        Language.NO_NB: "Markedsplass",
        Language.NO_NN: "Marknadsplassen",
        Language.SV_SE: "Marknadsplats",
        Language.DA_DK: "Markedsplads",
        Language.FI_FI: "Markkinapaikka",
        Language.DE_DE: "Marktplatz",
    },
    "nav.academy": {
        Language.EN_US: "Academy",
        Language.EN_GB: "Academy",
        Language.NO_NB: "Akademi",
        Language.NO_NN: "Akademi",
        Language.SV_SE: "Akademi",
        Language.DA_DK: "Akademi",
        Language.FI_FI: "Akatemia",
        Language.DE_DE: "Akademie",
    },
    "nav.analytics": {
        Language.EN_US: "Analytics",
        Language.EN_GB: "Analytics",
        Language.NO_NB: "Analyser",
        Language.NO_NN: "Analysar",
        Language.SV_SE: "Analyser",
        Language.DA_DK: "Analyser",
        Language.FI_FI: "Analytiikka",
        Language.DE_DE: "Analysen",
    },

    # ========================================================================
    # AUTHENTICATION
    # ========================================================================
    "auth.login": {
        Language.EN_US: "Log in",
        Language.EN_GB: "Log in",
        Language.NO_NB: "Logg inn",
        Language.NO_NN: "Logg inn",
        Language.SV_SE: "Logga in",
        Language.DA_DK: "Log ind",
        Language.FI_FI: "Kirjaudu sisään",
        Language.DE_DE: "Anmelden",
    },
    "auth.signup": {
        Language.EN_US: "Sign up",
        Language.EN_GB: "Sign up",
        Language.NO_NB: "Registrer deg",
        Language.NO_NN: "Registrer deg",
        Language.SV_SE: "Registrera dig",
        Language.DA_DK: "Tilmeld dig",
        Language.FI_FI: "Rekisteröidy",
        Language.DE_DE: "Registrieren",
    },
    "auth.email": {
        Language.EN_US: "Email",
        Language.EN_GB: "Email",
        Language.NO_NB: "E-post",
        Language.NO_NN: "E-post",
        Language.SV_SE: "E-post",
        Language.DA_DK: "E-mail",
        Language.FI_FI: "Sähköposti",
        Language.DE_DE: "E-Mail",
    },
    "auth.password": {
        Language.EN_US: "Password",
        Language.EN_GB: "Password",
        Language.NO_NB: "Passord",
        Language.NO_NN: "Passord",
        Language.SV_SE: "Lösenord",
        Language.DA_DK: "Adgangskode",
        Language.FI_FI: "Salasana",
        Language.DE_DE: "Passwort",
    },

    # ========================================================================
    # PRICING
    # ========================================================================
    "pricing.free": {
        Language.EN_US: "Free",
        Language.EN_GB: "Free",
        Language.NO_NB: "Gratis",
        Language.NO_NN: "Gratis",
        Language.SV_SE: "Gratis",
        Language.DA_DK: "Gratis",
        Language.FI_FI: "Ilmainen",
        Language.DE_DE: "Kostenlos",
    },
    "pricing.pro": {
        Language.EN_US: "Pro",
        Language.EN_GB: "Pro",
        Language.NO_NB: "Pro",
        Language.NO_NN: "Pro",
        Language.SV_SE: "Pro",
        Language.DA_DK: "Pro",
        Language.FI_FI: "Pro",
        Language.DE_DE: "Pro",
    },
    "pricing.enterprise": {
        Language.EN_US: "Enterprise",
        Language.EN_GB: "Enterprise",
        Language.NO_NB: "Enterprise",
        Language.NO_NN: "Enterprise",
        Language.SV_SE: "Enterprise",
        Language.DA_DK: "Enterprise",
        Language.FI_FI: "Enterprise",
        Language.DE_DE: "Enterprise",
    },
    "pricing.per_month": {
        Language.EN_US: "per month",
        Language.EN_GB: "per month",
        Language.NO_NB: "per måned",
        Language.NO_NN: "per månad",
        Language.SV_SE: "per månad",
        Language.DA_DK: "per måned",
        Language.FI_FI: "kuukaudessa",
        Language.DE_DE: "pro Monat",
    },
    "pricing.get_started": {
        Language.EN_US: "Get Started",
        Language.EN_GB: "Get Started",
        Language.NO_NB: "Kom i gang",
        Language.NO_NN: "Kom i gang",
        Language.SV_SE: "Kom igång",
        Language.DA_DK: "Kom i gang",
        Language.FI_FI: "Aloita",
        Language.DE_DE: "Jetzt starten",
    },

    # ========================================================================
    # AGENTS
    # ========================================================================
    "agents.create": {
        Language.EN_US: "Create Agent",
        Language.EN_GB: "Create Agent",
        Language.NO_NB: "Opprett agent",
        Language.NO_NN: "Opprett agent",
        Language.SV_SE: "Skapa agent",
        Language.DA_DK: "Opret agent",
        Language.FI_FI: "Luo agentti",
        Language.DE_DE: "Agent erstellen",
    },
    "agents.deploy": {
        Language.EN_US: "Deploy",
        Language.EN_GB: "Deploy",
        Language.NO_NB: "Distribuer",
        Language.NO_NN: "Distribuer",
        Language.SV_SE: "Distribuera",
        Language.DA_DK: "Udrulning",
        Language.FI_FI: "Käyttöönotto",
        Language.DE_DE: "Bereitstellen",
    },
    "agents.active": {
        Language.EN_US: "Active",
        Language.EN_GB: "Active",
        Language.NO_NB: "Aktiv",
        Language.NO_NN: "Aktiv",
        Language.SV_SE: "Aktiv",
        Language.DA_DK: "Aktiv",
        Language.FI_FI: "Aktiivinen",
        Language.DE_DE: "Aktiv",
    },

    # ========================================================================
    # ACTIONS
    # ========================================================================
    "actions.save": {
        Language.EN_US: "Save",
        Language.EN_GB: "Save",
        Language.NO_NB: "Lagre",
        Language.NO_NN: "Lagre",
        Language.SV_SE: "Spara",
        Language.DA_DK: "Gem",
        Language.FI_FI: "Tallenna",
        Language.DE_DE: "Speichern",
    },
    "actions.cancel": {
        Language.EN_US: "Cancel",
        Language.EN_GB: "Cancel",
        Language.NO_NB: "Avbryt",
        Language.NO_NN: "Avbryt",
        Language.SV_SE: "Avbryt",
        Language.DA_DK: "Annuller",
        Language.FI_FI: "Peruuta",
        Language.DE_DE: "Abbrechen",
    },
    "actions.delete": {
        Language.EN_US: "Delete",
        Language.EN_GB: "Delete",
        Language.NO_NB: "Slett",
        Language.NO_NN: "Slett",
        Language.SV_SE: "Ta bort",
        Language.DA_DK: "Slet",
        Language.FI_FI: "Poista",
        Language.DE_DE: "Löschen",
    },
    "actions.edit": {
        Language.EN_US: "Edit",
        Language.EN_GB: "Edit",
        Language.NO_NB: "Rediger",
        Language.NO_NN: "Rediger",
        Language.SV_SE: "Redigera",
        Language.DA_DK: "Rediger",
        Language.FI_FI: "Muokkaa",
        Language.DE_DE: "Bearbeiten",
    },

    # ========================================================================
    # NOTIFICATIONS
    # ========================================================================
    "notifications.success": {
        Language.EN_US: "Success!",
        Language.EN_GB: "Success!",
        Language.NO_NB: "Suksess!",
        Language.NO_NN: "Suksess!",
        Language.SV_SE: "Framgång!",
        Language.DA_DK: "Succes!",
        Language.FI_FI: "Onnistui!",
        Language.DE_DE: "Erfolg!",
    },
    "notifications.error": {
        Language.EN_US: "Error",
        Language.EN_GB: "Error",
        Language.NO_NB: "Feil",
        Language.NO_NN: "Feil",
        Language.SV_SE: "Fel",
        Language.DA_DK: "Fejl",
        Language.FI_FI: "Virhe",
        Language.DE_DE: "Fehler",
    },

    # ========================================================================
    # ACADEMY
    # ========================================================================
    "academy.courses": {
        Language.EN_US: "Courses",
        Language.EN_GB: "Courses",
        Language.NO_NB: "Kurs",
        Language.NO_NN: "Kurs",
        Language.SV_SE: "Kurser",
        Language.DA_DK: "Kurser",
        Language.FI_FI: "Kurssit",
        Language.DE_DE: "Kurse",
    },
    "academy.start_course": {
        Language.EN_US: "Start Course",
        Language.EN_GB: "Start Course",
        Language.NO_NB: "Start kurs",
        Language.NO_NN: "Start kurs",
        Language.SV_SE: "Starta kurs",
        Language.DA_DK: "Start kursus",
        Language.FI_FI: "Aloita kurssi",
        Language.DE_DE: "Kurs starten",
    },
    "academy.certificate": {
        Language.EN_US: "Certificate",
        Language.EN_GB: "Certificate",
        Language.NO_NB: "Sertifikat",
        Language.NO_NN: "Sertifikat",
        Language.SV_SE: "Certifikat",
        Language.DA_DK: "Certifikat",
        Language.FI_FI: "Sertifikaatti",
        Language.DE_DE: "Zertifikat",
    },

    # ========================================================================
    # WELCOME MESSAGES
    # ========================================================================
    "welcome.title": {
        Language.EN_US: "Welcome to Mindframe",
        Language.EN_GB: "Welcome to Mindframe",
        Language.NO_NB: "Velkommen til Mindframe",
        Language.NO_NN: "Velkommen til Mindframe",
        Language.SV_SE: "Välkommen till Mindframe",
        Language.DA_DK: "Velkommen til Mindframe",
        Language.FI_FI: "Tervetuloa Mindframeen",
        Language.DE_DE: "Willkommen bei Mindframe",
    },
    "welcome.subtitle": {
        Language.EN_US: "AI-Powered Agent Automation Platform",
        Language.EN_GB: "AI-Powered Agent Automation Platform",
        Language.NO_NB: "AI-drevet plattform for agentautomatisering",
        Language.NO_NN: "AI-driven plattform for agentautomatisering",
        Language.SV_SE: "AI-driven plattform för agentautomation",
        Language.DA_DK: "AI-drevet platform til agentautomatisering",
        Language.FI_FI: "AI-pohjainen agenttiautomaatioalusta",
        Language.DE_DE: "KI-gestützte Agentenautomatisierungsplattform",
    },
}


# ============================================================================
# CURRENCY & NUMBER FORMATTING
# ============================================================================

CURRENCY_FORMATS = {
    Language.EN_US: {"symbol": "$", "position": "before", "decimal": ".", "thousands": ","},
    Language.EN_GB: {"symbol": "£", "position": "before", "decimal": ".", "thousands": ","},
    Language.NO_NB: {"symbol": "kr", "position": "after", "decimal": ",", "thousands": " "},
    Language.NO_NN: {"symbol": "kr", "position": "after", "decimal": ",", "thousands": " "},
    Language.SV_SE: {"symbol": "kr", "position": "after", "decimal": ",", "thousands": " "},
    Language.DA_DK: {"symbol": "kr", "position": "after", "decimal": ",", "thousands": "."},
    Language.FI_FI: {"symbol": "€", "position": "after", "decimal": ",", "thousands": " "},
    Language.DE_DE: {"symbol": "€", "position": "after", "decimal": ",", "thousands": "."},
}


# ============================================================================
# DATE FORMATS
# ============================================================================

DATE_FORMATS = {
    Language.EN_US: "%m/%d/%Y",  # 12/31/2024
    Language.EN_GB: "%d/%m/%Y",  # 31/12/2024
    Language.NO_NB: "%d.%m.%Y",  # 31.12.2024
    Language.NO_NN: "%d.%m.%Y",  # 31.12.2024
    Language.SV_SE: "%Y-%m-%d",  # 2024-12-31
    Language.DA_DK: "%d-%m-%Y",  # 31-12-2024
    Language.FI_FI: "%d.%m.%Y",  # 31.12.2024
    Language.DE_DE: "%d.%m.%Y",  # 31.12.2024
}


# ============================================================================
# TRANSLATION FUNCTIONS
# ============================================================================

class Translator:
    """Translation helper class"""

    def __init__(self, language: Language = Language.EN_US):
        self.language = language

    def translate(self, key: str, **kwargs) -> str:
        """
        Translate a key to current language

        Args:
            key: Translation key (e.g., "nav.dashboard")
            **kwargs: Optional format arguments

        Returns:
            Translated string
        """
        translation = TRANSLATIONS.get(key, {}).get(self.language)

        if not translation:
            # Fallback to English
            translation = TRANSLATIONS.get(key, {}).get(Language.EN_US, key)

        # Format with kwargs if provided
        if kwargs:
            translation = translation.format(**kwargs)

        return translation

    def t(self, key: str, **kwargs) -> str:
        """Shorthand for translate()"""
        return self.translate(key, **kwargs)

    def format_currency(self, amount: float) -> str:
        """Format currency according to language"""
        fmt = CURRENCY_FORMATS.get(self.language, CURRENCY_FORMATS[Language.EN_US])

        # Format number
        if fmt["decimal"] == ",":
            formatted = f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", fmt["thousands"])
        else:
            formatted = f"{amount:,.2f}"

        # Add currency symbol
        if fmt["position"] == "before":
            return f"{fmt['symbol']}{formatted}"
        else:
            return f"{formatted} {fmt['symbol']}"

    def format_date(self, date) -> str:
        """Format date according to language"""
        fmt = DATE_FORMATS.get(self.language, DATE_FORMATS[Language.EN_US])
        return date.strftime(fmt)

    def get_language_name(self) -> str:
        """Get language display name"""
        names = {
            Language.EN_US: "English (US)",
            Language.EN_GB: "English (UK)",
            Language.NO_NB: "Norsk (Bokmål)",
            Language.NO_NN: "Norsk (Nynorsk)",
            Language.SV_SE: "Svenska",
            Language.DA_DK: "Dansk",
            Language.FI_FI: "Suomi",
            Language.DE_DE: "Deutsch",
        }
        return names.get(self.language, "English")


# ============================================================================
# LANGUAGE DETECTION
# ============================================================================

def detect_language_from_request(request) -> Language:
    """
    Detect language from HTTP request

    Checks:
    1. URL parameter (?lang=no_NB)
    2. Cookie
    3. Accept-Language header
    4. Default to English
    """
    # Check URL parameter
    lang_param = request.query_params.get("lang")
    if lang_param:
        try:
            return Language(lang_param)
        except ValueError:
            pass

    # Check cookie
    lang_cookie = request.cookies.get("language")
    if lang_cookie:
        try:
            return Language(lang_cookie)
        except ValueError:
            pass

    # Check Accept-Language header
    accept_language = request.headers.get("Accept-Language", "")
    if "no" in accept_language.lower() or "nb" in accept_language.lower():
        return Language.NO_NB
    elif "nn" in accept_language.lower():
        return Language.NO_NN
    elif "sv" in accept_language.lower():
        return Language.SV_SE
    elif "da" in accept_language.lower():
        return Language.DA_DK
    elif "fi" in accept_language.lower():
        return Language.FI_FI
    elif "de" in accept_language.lower():
        return Language.DE_DE
    elif "en-gb" in accept_language.lower():
        return Language.EN_GB

    # Default to US English
    return Language.EN_US


def get_supported_languages() -> list:
    """Get list of all supported languages"""
    return [
        {"code": Language.EN_US, "name": "English (US)", "flag": "🇺🇸"},
        {"code": Language.EN_GB, "name": "English (UK)", "flag": "🇬🇧"},
        {"code": Language.NO_NB, "name": "Norsk (Bokmål)", "flag": "🇳🇴"},
        {"code": Language.NO_NN, "name": "Norsk (Nynorsk)", "flag": "🇳🇴"},
        {"code": Language.SV_SE, "name": "Svenska", "flag": "🇸🇪"},
        {"code": Language.DA_DK, "name": "Dansk", "flag": "🇩🇰"},
        {"code": Language.FI_FI, "name": "Suomi", "flag": "🇫🇮"},
        {"code": Language.DE_DE, "name": "Deutsch", "flag": "🇩🇪"},
    ]


# ============================================================================
# FASTAPI DEPENDENCY
# ============================================================================

def get_translator(request) -> Translator:
    """
    FastAPI dependency to get translator

    Usage:
        @app.get("/")
        def index(t: Translator = Depends(get_translator)):
            return {"title": t.t("welcome.title")}
    """
    language = detect_language_from_request(request)
    return Translator(language)


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'Language',
    'Translator',
    'TRANSLATIONS',
    'detect_language_from_request',
    'get_supported_languages',
    'get_translator'
]
