"""
GDPR-Compliant Cookie Consent Manager
Granular cookie consent for EU/EEA markets
"""
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import json


# ============================================================================
# COOKIE CATEGORIES
# ============================================================================

class CookieCategory(str, Enum):
    """Cookie categories per GDPR requirements"""
    NECESSARY = "necessary"  # Always allowed, cannot be disabled
    FUNCTIONAL = "functional"  # Remember preferences
    ANALYTICS = "analytics"  # Usage statistics
    MARKETING = "marketing"  # Advertising and tracking
    PERFORMANCE = "performance"  # Performance monitoring


# ============================================================================
# COOKIE DEFINITIONS
# ============================================================================

COOKIE_DEFINITIONS = {
    # Necessary cookies (always active)
    "session_id": {
        "name": "session_id",
        "category": CookieCategory.NECESSARY,
        "purpose": "Maintains your login session",
        "duration": "Session",
        "required": True
    },
    "csrf_token": {
        "name": "csrf_token",
        "category": CookieCategory.NECESSARY,
        "purpose": "Security - prevents cross-site request forgery",
        "duration": "Session",
        "required": True
    },
    "cookie_consent": {
        "name": "cookie_consent",
        "category": CookieCategory.NECESSARY,
        "purpose": "Stores your cookie preferences",
        "duration": "1 year",
        "required": True
    },

    # Functional cookies
    "language": {
        "name": "language",
        "category": CookieCategory.FUNCTIONAL,
        "purpose": "Remembers your language preference",
        "duration": "1 year",
        "required": False
    },
    "theme": {
        "name": "theme",
        "category": CookieCategory.FUNCTIONAL,
        "purpose": "Remembers your theme (light/dark mode)",
        "duration": "1 year",
        "required": False
    },
    "dashboard_layout": {
        "name": "dashboard_layout",
        "category": CookieCategory.FUNCTIONAL,
        "purpose": "Remembers your dashboard layout preferences",
        "duration": "6 months",
        "required": False
    },

    # Analytics cookies
    "_ga": {
        "name": "_ga",
        "category": CookieCategory.ANALYTICS,
        "purpose": "Google Analytics - user identification",
        "duration": "2 years",
        "required": False,
        "third_party": "Google"
    },
    "_ga_*": {
        "name": "_ga_*",
        "category": CookieCategory.ANALYTICS,
        "purpose": "Google Analytics - session tracking",
        "duration": "2 years",
        "required": False,
        "third_party": "Google"
    },
    "mixpanel": {
        "name": "mixpanel",
        "category": CookieCategory.ANALYTICS,
        "purpose": "Mixpanel analytics - user behavior tracking",
        "duration": "1 year",
        "required": False,
        "third_party": "Mixpanel"
    },

    # Marketing cookies
    "_fbp": {
        "name": "_fbp",
        "category": CookieCategory.MARKETING,
        "purpose": "Facebook Pixel - ad targeting",
        "duration": "3 months",
        "required": False,
        "third_party": "Facebook"
    },
    "_gcl_au": {
        "name": "_gcl_au",
        "category": CookieCategory.MARKETING,
        "purpose": "Google Ads - conversion tracking",
        "duration": "3 months",
        "required": False,
        "third_party": "Google"
    },
    "linkedin_cookie": {
        "name": "linkedin_cookie",
        "category": CookieCategory.MARKETING,
        "purpose": "LinkedIn Ads - professional targeting",
        "duration": "6 months",
        "required": False,
        "third_party": "LinkedIn"
    },

    # Performance cookies
    "sentry_session": {
        "name": "sentry_session",
        "category": CookieCategory.PERFORMANCE,
        "purpose": "Sentry error tracking - improves app reliability",
        "duration": "Session",
        "required": False,
        "third_party": "Sentry"
    }
}


# ============================================================================
# CONSENT MODELS
# ============================================================================

class ConsentPreferences(BaseModel):
    """User's cookie consent preferences"""
    necessary: bool = True  # Always true, cannot be disabled
    functional: bool = False
    analytics: bool = False
    marketing: bool = False
    performance: bool = False
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class CookieConsentManager:
    """Manages cookie consent for GDPR compliance"""

    @staticmethod
    def get_default_preferences() -> ConsentPreferences:
        """Get default consent (only necessary cookies)"""
        return ConsentPreferences(
            necessary=True,
            functional=False,
            analytics=False,
            marketing=False,
            performance=False,
            timestamp=datetime.utcnow()
        )

    @staticmethod
    def get_accept_all_preferences() -> ConsentPreferences:
        """Get accept-all consent"""
        return ConsentPreferences(
            necessary=True,
            functional=True,
            analytics=True,
            marketing=True,
            performance=True,
            timestamp=datetime.utcnow()
        )

    @staticmethod
    def encode_preferences(prefs: ConsentPreferences) -> str:
        """Encode preferences to cookie string"""
        data = {
            "necessary": prefs.necessary,
            "functional": prefs.functional,
            "analytics": prefs.analytics,
            "marketing": prefs.marketing,
            "performance": prefs.performance,
            "timestamp": prefs.timestamp.isoformat()
        }
        return json.dumps(data)

    @staticmethod
    def decode_preferences(cookie_string: str) -> ConsentPreferences:
        """Decode preferences from cookie string"""
        try:
            data = json.loads(cookie_string)
            return ConsentPreferences(
                necessary=data.get("necessary", True),
                functional=data.get("functional", False),
                analytics=data.get("analytics", False),
                marketing=data.get("marketing", False),
                performance=data.get("performance", False),
                timestamp=datetime.fromisoformat(data["timestamp"])
            )
        except:
            return CookieConsentManager.get_default_preferences()

    @staticmethod
    def is_consent_valid(prefs: ConsentPreferences, max_age_days: int = 365) -> bool:
        """Check if consent is still valid (not expired)"""
        age = datetime.utcnow() - prefs.timestamp
        return age.days < max_age_days

    @staticmethod
    def get_allowed_cookies(prefs: ConsentPreferences) -> List[str]:
        """Get list of allowed cookie names based on consent"""
        allowed = []

        for cookie_name, cookie_def in COOKIE_DEFINITIONS.items():
            category = cookie_def["category"]

            # Always allow necessary cookies
            if category == CookieCategory.NECESSARY:
                allowed.append(cookie_name)
            elif category == CookieCategory.FUNCTIONAL and prefs.functional:
                allowed.append(cookie_name)
            elif category == CookieCategory.ANALYTICS and prefs.analytics:
                allowed.append(cookie_name)
            elif category == CookieCategory.MARKETING and prefs.marketing:
                allowed.append(cookie_name)
            elif category == CookieCategory.PERFORMANCE and prefs.performance:
                allowed.append(cookie_name)

        return allowed

    @staticmethod
    def get_cookie_policy_text(language: str = "en") -> Dict:
        """Get cookie policy text for display"""
        policies = {
            "en": {
                "title": "Cookie Policy",
                "intro": "We use cookies to improve your experience on our platform.",
                "categories": {
                    "necessary": {
                        "title": "Necessary Cookies",
                        "description": "These cookies are essential for the website to function and cannot be disabled."
                    },
                    "functional": {
                        "title": "Functional Cookies",
                        "description": "These cookies remember your preferences and choices."
                    },
                    "analytics": {
                        "title": "Analytics Cookies",
                        "description": "These cookies help us understand how you use our website."
                    },
                    "marketing": {
                        "title": "Marketing Cookies",
                        "description": "These cookies are used to show you relevant advertisements."
                    },
                    "performance": {
                        "title": "Performance Cookies",
                        "description": "These cookies help us monitor and improve website performance."
                    }
                }
            },
            "no": {
                "title": "Informasjonskapsler (cookies)",
                "intro": "Vi bruker informasjonskapsler for å forbedre din opplevelse på plattformen.",
                "categories": {
                    "necessary": {
                        "title": "Nødvendige informasjonskapsler",
                        "description": "Disse informasjonskapslene er nødvendige for at nettstedet skal fungere og kan ikke deaktiveres."
                    },
                    "functional": {
                        "title": "Funksjonelle informasjonskapsler",
                        "description": "Disse informasjonskapslene husker dine preferanser og valg."
                    },
                    "analytics": {
                        "title": "Analyse-informasjonskapsler",
                        "description": "Disse informasjonskapslene hjelper oss å forstå hvordan du bruker nettstedet vårt."
                    },
                    "marketing": {
                        "title": "Markedsførings-informasjonskapsler",
                        "description": "Disse informasjonskapslene brukes til å vise deg relevante annonser."
                    },
                    "performance": {
                        "title": "Ytelses-informasjonskapsler",
                        "description": "Disse informasjonskapslene hjelper oss å overvåke og forbedre nettstedets ytelse."
                    }
                }
            }
        }

        return policies.get(language, policies["en"])

    @staticmethod
    def log_consent_change(
        user_id: Optional[int],
        old_prefs: Optional[ConsentPreferences],
        new_prefs: ConsentPreferences,
        ip_address: str,
        user_agent: str
    ):
        """Log consent changes for GDPR compliance audit trail"""
        # In production, store this in database
        log_entry = {
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "old_preferences": old_prefs.dict() if old_prefs else None,
            "new_preferences": new_prefs.dict(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "action": "consent_updated"
        }

        # TODO: Save to database for GDPR audit trail
        # db.consent_logs.insert(log_entry)

        return log_entry


# ============================================================================
# COOKIE BANNER CONFIGURATION
# ============================================================================

COOKIE_BANNER_CONFIG = {
    "position": "bottom",  # top or bottom
    "theme": "light",  # light or dark
    "layout": "block",  # block or inline
    "show_reject_button": True,
    "show_settings_button": True,
    "auto_close_on_accept": True,
    "banner_text": {
        "en": "We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.",
        "no": "Vi bruker informasjonskapsler for å forbedre din opplevelse. Ved å fortsette å besøke dette nettstedet godtar du vår bruk av informasjonskapsler."
    },
    "buttons": {
        "accept_all": {"en": "Accept All", "no": "Godta alle"},
        "reject_all": {"en": "Reject All", "no": "Avvis alle"},
        "customize": {"en": "Customize", "no": "Tilpass"},
        "save": {"en": "Save Preferences", "no": "Lagre preferanser"}
    }
}


# ============================================================================
# THIRD-PARTY SCRIPTS MANAGER
# ============================================================================

class ThirdPartyScriptsManager:
    """Manages loading of third-party scripts based on consent"""

    SCRIPTS = {
        CookieCategory.ANALYTICS: [
            {
                "name": "Google Analytics",
                "id": "google-analytics",
                "src": "https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID",
                "init_code": """
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
                    gtag('config', 'GA_MEASUREMENT_ID');
                """
            },
            {
                "name": "Mixpanel",
                "id": "mixpanel",
                "src": "https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js",
                "init_code": "mixpanel.init('YOUR_TOKEN');"
            }
        ],
        CookieCategory.MARKETING: [
            {
                "name": "Facebook Pixel",
                "id": "facebook-pixel",
                "src": "https://connect.facebook.net/en_US/fbevents.js",
                "init_code": "fbq('init', 'YOUR_PIXEL_ID'); fbq('track', 'PageView');"
            },
            {
                "name": "Google Ads",
                "id": "google-ads",
                "src": "https://www.googletagmanager.com/gtag/js?id=AW-CONVERSION_ID",
                "init_code": "gtag('config', 'AW-CONVERSION_ID');"
            }
        ],
        CookieCategory.PERFORMANCE: [
            {
                "name": "Sentry",
                "id": "sentry",
                "src": "https://js.sentry-cdn.com/YOUR_DSN.min.js",
                "init_code": "Sentry.init({ dsn: 'YOUR_DSN' });"
            }
        ]
    }

    @staticmethod
    def get_scripts_for_category(category: CookieCategory) -> List[Dict]:
        """Get all scripts for a specific category"""
        return ThirdPartyScriptsManager.SCRIPTS.get(category, [])

    @staticmethod
    def get_allowed_scripts(prefs: ConsentPreferences) -> List[Dict]:
        """Get all scripts that are allowed based on consent"""
        allowed_scripts = []

        if prefs.analytics:
            allowed_scripts.extend(
                ThirdPartyScriptsManager.get_scripts_for_category(CookieCategory.ANALYTICS)
            )

        if prefs.marketing:
            allowed_scripts.extend(
                ThirdPartyScriptsManager.get_scripts_for_category(CookieCategory.MARKETING)
            )

        if prefs.performance:
            allowed_scripts.extend(
                ThirdPartyScriptsManager.get_scripts_for_category(CookieCategory.PERFORMANCE)
            )

        return allowed_scripts


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'CookieCategory',
    'ConsentPreferences',
    'CookieConsentManager',
    'COOKIE_DEFINITIONS',
    'COOKIE_BANNER_CONFIG',
    'ThirdPartyScriptsManager'
]
