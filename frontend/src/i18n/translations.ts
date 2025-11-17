/**
 * Multi-Language Support for Mindframe Frontend
 * Internationalization (i18n) for Nordic and European markets
 */

export enum Language {
  EN_US = 'en_US', // English (United States)
  EN_GB = 'en_GB', // English (United Kingdom)
  NO_NB = 'no_NB', // Norwegian Bokmål
  NO_NN = 'no_NN', // Norwegian Nynorsk
  SV_SE = 'sv_SE', // Swedish
  DA_DK = 'da_DK', // Danish
  FI_FI = 'fi_FI', // Finnish
  DE_DE = 'de_DE', // German
}

export const translations = {
  // Navigation
  'nav.dashboard': {
    [Language.EN_US]: 'Dashboard',
    [Language.EN_GB]: 'Dashboard',
    [Language.NO_NB]: 'Dashbord',
    [Language.NO_NN]: 'Dashbord',
    [Language.SV_SE]: 'Instrumentpanel',
    [Language.DA_DK]: 'Dashboard',
    [Language.FI_FI]: 'Kojelauta',
    [Language.DE_DE]: 'Dashboard',
  },
  'nav.agents': {
    [Language.EN_US]: 'AI Agents',
    [Language.EN_GB]: 'AI Agents',
    [Language.NO_NB]: 'AI-agenter',
    [Language.NO_NN]: 'AI-agentar',
    [Language.SV_SE]: 'AI-agenter',
    [Language.DA_DK]: 'AI-agenter',
    [Language.FI_FI]: 'AI-agentit',
    [Language.DE_DE]: 'KI-Agenten',
  },
  'nav.marketplace': {
    [Language.EN_US]: 'Marketplace',
    [Language.EN_GB]: 'Marketplace',
    [Language.NO_NB]: 'Markedsplass',
    [Language.NO_NN]: 'Marknadsplassen',
    [Language.SV_SE]: 'Marknadsplats',
    [Language.DA_DK]: 'Markedsplads',
    [Language.FI_FI]: 'Markkinapaikka',
    [Language.DE_DE]: 'Marktplatz',
  },
  'nav.academy': {
    [Language.EN_US]: 'Academy',
    [Language.EN_GB]: 'Academy',
    [Language.NO_NB]: 'Akademi',
    [Language.NO_NN]: 'Akademi',
    [Language.SV_SE]: 'Akademi',
    [Language.DA_DK]: 'Akademi',
    [Language.FI_FI]: 'Akatemia',
    [Language.DE_DE]: 'Akademie',
  },
  'nav.analytics': {
    [Language.EN_US]: 'Analytics',
    [Language.EN_GB]: 'Analytics',
    [Language.NO_NB]: 'Analyser',
    [Language.NO_NN]: 'Analysar',
    [Language.SV_SE]: 'Analyser',
    [Language.DA_DK]: 'Analyser',
    [Language.FI_FI]: 'Analytiikka',
    [Language.DE_DE]: 'Analysen',
  },
  // Authentication
  'auth.login': {
    [Language.EN_US]: 'Log in',
    [Language.EN_GB]: 'Log in',
    [Language.NO_NB]: 'Logg inn',
    [Language.NO_NN]: 'Logg inn',
    [Language.SV_SE]: 'Logga in',
    [Language.DA_DK]: 'Log ind',
    [Language.FI_FI]: 'Kirjaudu sisään',
    [Language.DE_DE]: 'Anmelden',
  },
  'auth.signup': {
    [Language.EN_US]: 'Sign up',
    [Language.EN_GB]: 'Sign up',
    [Language.NO_NB]: 'Registrer deg',
    [Language.NO_NN]: 'Registrer deg',
    [Language.SV_SE]: 'Registrera dig',
    [Language.DA_DK]: 'Tilmeld dig',
    [Language.FI_FI]: 'Rekisteröidy',
    [Language.DE_DE]: 'Registrieren',
  },
  'welcome.title': {
    [Language.EN_US]: 'Welcome to Mindframe',
    [Language.EN_GB]: 'Welcome to Mindframe',
    [Language.NO_NB]: 'Velkommen til Mindframe',
    [Language.NO_NN]: 'Velkommen til Mindframe',
    [Language.SV_SE]: 'Välkommen till Mindframe',
    [Language.DA_DK]: 'Velkommen til Mindframe',
    [Language.FI_FI]: 'Tervetuloa Mindframeen',
    [Language.DE_DE]: 'Willkommen bei Mindframe',
  },
  'welcome.subtitle': {
    [Language.EN_US]: 'AI-Powered Agent Automation Platform',
    [Language.EN_GB]: 'AI-Powered Agent Automation Platform',
    [Language.NO_NB]: 'AI-drevet plattform for agentautomatisering',
    [Language.NO_NN]: 'AI-driven plattform for agentautomatisering',
    [Language.SV_SE]: 'AI-driven plattform för agentautomation',
    [Language.DA_DK]: 'AI-drevet platform til agentautomatisering',
    [Language.FI_FI]: 'AI-pohjainen agenttiautomaatioalusta',
    [Language.DE_DE]: 'KI-gestützte Agentenautomatisierungsplattform',
  },
  'pricing.per_month': {
    [Language.EN_US]: 'per month',
    [Language.EN_GB]: 'per month',
    [Language.NO_NB]: 'per måned',
    [Language.NO_NN]: 'per månad',
    [Language.SV_SE]: 'per månad',
    [Language.DA_DK]: 'per måned',
    [Language.FI_FI]: 'kuukaudessa',
    [Language.DE_DE]: 'pro Monat',
  },
  'pricing.get_started': {
    [Language.EN_US]: 'Get Started',
    [Language.EN_GB]: 'Get Started',
    [Language.NO_NB]: 'Kom i gang',
    [Language.NO_NN]: 'Kom i gang',
    [Language.SV_SE]: 'Kom igång',
    [Language.DA_DK]: 'Kom i gang',
    [Language.FI_FI]: 'Aloita',
    [Language.DE_DE]: 'Jetzt starten',
  },
  // Cookie Consent
  'cookie.title': {
    [Language.EN_US]: 'Cookie Preferences',
    [Language.EN_GB]: 'Cookie Preferences',
    [Language.NO_NB]: 'Informasjonskapsler',
    [Language.NO_NN]: 'Informasjonskapslar',
    [Language.SV_SE]: 'Cookie-inställningar',
    [Language.DA_DK]: 'Cookie-præferencer',
    [Language.FI_FI]: 'Evästeasetukset',
    [Language.DE_DE]: 'Cookie-Einstellungen',
  },
  'cookie.description': {
    [Language.EN_US]: 'We use cookies to enhance your experience on our platform. You can customize your preferences or accept all cookies.',
    [Language.EN_GB]: 'We use cookies to enhance your experience on our platform. You can customise your preferences or accept all cookies.',
    [Language.NO_NB]: 'Vi bruker informasjonskapsler for å forbedre din opplevelse på plattformen. Du kan tilpasse dine preferanser eller godta alle informasjonskapsler.',
    [Language.NO_NN]: 'Vi bruker informasjonskapslar for å forbetre di oppleving på plattforma. Du kan tilpasse preferansane dine eller godta alle informasjonskapslar.',
    [Language.SV_SE]: 'Vi använder cookies för att förbättra din upplevelse på vår plattform. Du kan anpassa dina preferenser eller acceptera alla cookies.',
    [Language.DA_DK]: 'Vi bruger cookies for at forbedre din oplevelse på vores platform. Du kan tilpasse dine præferencer eller acceptere alle cookies.',
    [Language.FI_FI]: 'Käytämme evästeitä parantaaksemme kokemustasi alustalla. Voit mukauttaa asetuksiasi tai hyväksyä kaikki evästeet.',
    [Language.DE_DE]: 'Wir verwenden Cookies, um Ihre Erfahrung auf unserer Plattform zu verbessern. Sie können Ihre Präferenzen anpassen oder alle Cookies akzeptieren.',
  },
  'cookie.learn_more': {
    [Language.EN_US]: 'Learn more',
    [Language.EN_GB]: 'Learn more',
    [Language.NO_NB]: 'Les mer',
    [Language.NO_NN]: 'Les meir',
    [Language.SV_SE]: 'Läs mer',
    [Language.DA_DK]: 'Læs mere',
    [Language.FI_FI]: 'Lue lisää',
    [Language.DE_DE]: 'Mehr erfahren',
  },
  'cookie.accept_all': {
    [Language.EN_US]: 'Accept All',
    [Language.EN_GB]: 'Accept All',
    [Language.NO_NB]: 'Godta alle',
    [Language.NO_NN]: 'Godta alle',
    [Language.SV_SE]: 'Acceptera alla',
    [Language.DA_DK]: 'Acceptér alle',
    [Language.FI_FI]: 'Hyväksy kaikki',
    [Language.DE_DE]: 'Alle akzeptieren',
  },
  'cookie.reject_all': {
    [Language.EN_US]: 'Reject All',
    [Language.EN_GB]: 'Reject All',
    [Language.NO_NB]: 'Avvis alle',
    [Language.NO_NN]: 'Avvis alle',
    [Language.SV_SE]: 'Avvisa alla',
    [Language.DA_DK]: 'Afvis alle',
    [Language.FI_FI]: 'Hylkää kaikki',
    [Language.DE_DE]: 'Alle ablehnen',
  },
  'cookie.customize': {
    [Language.EN_US]: 'Customize',
    [Language.EN_GB]: 'Customise',
    [Language.NO_NB]: 'Tilpass',
    [Language.NO_NN]: 'Tilpass',
    [Language.SV_SE]: 'Anpassa',
    [Language.DA_DK]: 'Tilpas',
    [Language.FI_FI]: 'Mukauta',
    [Language.DE_DE]: 'Anpassen',
  },
  'cookie.customize_title': {
    [Language.EN_US]: 'Customize Cookie Preferences',
    [Language.EN_GB]: 'Customise Cookie Preferences',
    [Language.NO_NB]: 'Tilpass informasjonskapsler',
    [Language.NO_NN]: 'Tilpass informasjonskapslar',
    [Language.SV_SE]: 'Anpassa cookie-inställningar',
    [Language.DA_DK]: 'Tilpas cookie-præferencer',
    [Language.FI_FI]: 'Mukauta evästeasetuksia',
    [Language.DE_DE]: 'Cookie-Einstellungen anpassen',
  },
  'cookie.save_preferences': {
    [Language.EN_US]: 'Save Preferences',
    [Language.EN_GB]: 'Save Preferences',
    [Language.NO_NB]: 'Lagre preferanser',
    [Language.NO_NN]: 'Lagre preferansar',
    [Language.SV_SE]: 'Spara preferenser',
    [Language.DA_DK]: 'Gem præferencer',
    [Language.FI_FI]: 'Tallenna asetukset',
    [Language.DE_DE]: 'Einstellungen speichern',
  },
  'cookie.always_active': {
    [Language.EN_US]: 'Always Active',
    [Language.EN_GB]: 'Always Active',
    [Language.NO_NB]: 'Alltid aktiv',
    [Language.NO_NN]: 'Alltid aktiv',
    [Language.SV_SE]: 'Alltid aktiv',
    [Language.DA_DK]: 'Altid aktiv',
    [Language.FI_FI]: 'Aina aktiivinen',
    [Language.DE_DE]: 'Immer aktiv',
  },
  'cookie.necessary_title': {
    [Language.EN_US]: 'Necessary Cookies',
    [Language.EN_GB]: 'Necessary Cookies',
    [Language.NO_NB]: 'Nødvendige informasjonskapsler',
    [Language.NO_NN]: 'Nødvendige informasjonskapslar',
    [Language.SV_SE]: 'Nödvändiga cookies',
    [Language.DA_DK]: 'Nødvendige cookies',
    [Language.FI_FI]: 'Välttämättömät evästeet',
    [Language.DE_DE]: 'Notwendige Cookies',
  },
  'cookie.necessary_description': {
    [Language.EN_US]: 'These cookies are essential for the website to function and cannot be disabled.',
    [Language.EN_GB]: 'These cookies are essential for the website to function and cannot be disabled.',
    [Language.NO_NB]: 'Disse informasjonskapslene er nødvendige for at nettstedet skal fungere og kan ikke deaktiveres.',
    [Language.NO_NN]: 'Desse informasjonskapslane er nødvendige for at nettstaden skal fungere og kan ikkje deaktiverast.',
    [Language.SV_SE]: 'Dessa cookies är nödvändiga för att webbplatsen ska fungera och kan inte inaktiveras.',
    [Language.DA_DK]: 'Disse cookies er nødvendige for, at hjemmesiden fungerer, og kan ikke deaktiveres.',
    [Language.FI_FI]: 'Nämä evästeet ovat välttämättömiä verkkosivuston toiminnalle, eikä niitä voi poistaa käytöstä.',
    [Language.DE_DE]: 'Diese Cookies sind für die Funktion der Website unerlässlich und können nicht deaktiviert werden.',
  },
  'cookie.functional_title': {
    [Language.EN_US]: 'Functional Cookies',
    [Language.EN_GB]: 'Functional Cookies',
    [Language.NO_NB]: 'Funksjonelle informasjonskapsler',
    [Language.NO_NN]: 'Funksjonelle informasjonskapslar',
    [Language.SV_SE]: 'Funktionella cookies',
    [Language.DA_DK]: 'Funktionelle cookies',
    [Language.FI_FI]: 'Toiminnalliset evästeet',
    [Language.DE_DE]: 'Funktionale Cookies',
  },
  'cookie.functional_description': {
    [Language.EN_US]: 'These cookies remember your preferences and choices to provide a personalized experience.',
    [Language.EN_GB]: 'These cookies remember your preferences and choices to provide a personalised experience.',
    [Language.NO_NB]: 'Disse informasjonskapslene husker dine preferanser og valg for å gi deg en personlig opplevelse.',
    [Language.NO_NN]: 'Desse informasjonskapslane hugsar preferansane og vala dine for å gi deg ei personleg oppleving.',
    [Language.SV_SE]: 'Dessa cookies kommer ihåg dina preferenser och val för att ge en personlig upplevelse.',
    [Language.DA_DK]: 'Disse cookies husker dine præferencer og valg for at give en personlig oplevelse.',
    [Language.FI_FI]: 'Nämä evästeet muistavat asetuksesi ja valintasi tarjotakseen henkilökohtaisen kokemuksen.',
    [Language.DE_DE]: 'Diese Cookies merken sich Ihre Präferenzen und Auswahlmöglichkeiten, um ein personalisiertes Erlebnis zu bieten.',
  },
  'cookie.analytics_title': {
    [Language.EN_US]: 'Analytics Cookies',
    [Language.EN_GB]: 'Analytics Cookies',
    [Language.NO_NB]: 'Analyse-informasjonskapsler',
    [Language.NO_NN]: 'Analyse-informasjonskapslar',
    [Language.SV_SE]: 'Analyscookies',
    [Language.DA_DK]: 'Analysecookies',
    [Language.FI_FI]: 'Analytiikkaevästeet',
    [Language.DE_DE]: 'Analyse-Cookies',
  },
  'cookie.analytics_description': {
    [Language.EN_US]: 'These cookies help us understand how you use our website so we can improve it.',
    [Language.EN_GB]: 'These cookies help us understand how you use our website so we can improve it.',
    [Language.NO_NB]: 'Disse informasjonskapslene hjelper oss å forstå hvordan du bruker nettstedet vårt slik at vi kan forbedre det.',
    [Language.NO_NN]: 'Desse informasjonskapslane hjelper oss å forstå korleis du brukar nettstaden vår slik at vi kan forbetre han.',
    [Language.SV_SE]: 'Dessa cookies hjälper oss att förstå hur du använder vår webbplats så att vi kan förbättra den.',
    [Language.DA_DK]: 'Disse cookies hjælper os med at forstå, hvordan du bruger vores hjemmeside, så vi kan forbedre den.',
    [Language.FI_FI]: 'Nämä evästeet auttavat meitä ymmärtämään, miten käytät verkkosivustoamme, jotta voimme parantaa sitä.',
    [Language.DE_DE]: 'Diese Cookies helfen uns zu verstehen, wie Sie unsere Website nutzen, damit wir sie verbessern können.',
  },
  'cookie.marketing_title': {
    [Language.EN_US]: 'Marketing Cookies',
    [Language.EN_GB]: 'Marketing Cookies',
    [Language.NO_NB]: 'Markedsførings-informasjonskapsler',
    [Language.NO_NN]: 'Marknadsførings-informasjonskapslar',
    [Language.SV_SE]: 'Marknadsföringscookies',
    [Language.DA_DK]: 'Marketingcookies',
    [Language.FI_FI]: 'Markkinointievästeet',
    [Language.DE_DE]: 'Marketing-Cookies',
  },
  'cookie.marketing_description': {
    [Language.EN_US]: 'These cookies are used to show you relevant advertisements based on your interests.',
    [Language.EN_GB]: 'These cookies are used to show you relevant advertisements based on your interests.',
    [Language.NO_NB]: 'Disse informasjonskapslene brukes til å vise deg relevante annonser basert på dine interesser.',
    [Language.NO_NN]: 'Desse informasjonskapslane blir brukt til å vise deg relevante annonsar basert på interessene dine.',
    [Language.SV_SE]: 'Dessa cookies används för att visa dig relevanta annonser baserat på dina intressen.',
    [Language.DA_DK]: 'Disse cookies bruges til at vise dig relevante annoncer baseret på dine interesser.',
    [Language.FI_FI]: 'Näitä evästeitä käytetään näyttämään sinulle relevantteja mainoksia kiinnostuksesi perusteella.',
    [Language.DE_DE]: 'Diese Cookies werden verwendet, um Ihnen relevante Werbung basierend auf Ihren Interessen zu zeigen.',
  },
  'cookie.performance_title': {
    [Language.EN_US]: 'Performance Cookies',
    [Language.EN_GB]: 'Performance Cookies',
    [Language.NO_NB]: 'Ytelses-informasjonskapsler',
    [Language.NO_NN]: 'Ytelses-informasjonskapslar',
    [Language.SV_SE]: 'Prestandacookies',
    [Language.DA_DK]: 'Performancecookies',
    [Language.FI_FI]: 'Suorituskykyevästeet',
    [Language.DE_DE]: 'Leistungs-Cookies',
  },
  'cookie.performance_description': {
    [Language.EN_US]: 'These cookies help us monitor and improve website performance and reliability.',
    [Language.EN_GB]: 'These cookies help us monitor and improve website performance and reliability.',
    [Language.NO_NB]: 'Disse informasjonskapslene hjelper oss å overvåke og forbedre nettstedets ytelse og pålitelighet.',
    [Language.NO_NN]: 'Desse informasjonskapslane hjelper oss å overvake og forbetre nettstaden sin ytelse og pålitelegheit.',
    [Language.SV_SE]: 'Dessa cookies hjälper oss att övervaka och förbättra webbplatsens prestanda och tillförlitlighet.',
    [Language.DA_DK]: 'Disse cookies hjælper os med at overvåge og forbedre hjemmesidens ydeevne og pålidelighed.',
    [Language.FI_FI]: 'Nämä evästeet auttavat meitä valvomaan ja parantamaan verkkosivuston suorituskykyä ja luotettavuutta.',
    [Language.DE_DE]: 'Diese Cookies helfen uns, die Leistung und Zuverlässigkeit der Website zu überwachen und zu verbessern.',
  },
}

export const supportedLanguages = [
  { code: Language.EN_US, name: 'English (US)', flag: '🇺🇸' },
  { code: Language.EN_GB, name: 'English (UK)', flag: '🇬🇧' },
  { code: Language.NO_NB, name: 'Norsk (Bokmål)', flag: '🇳🇴' },
  { code: Language.NO_NN, name: 'Norsk (Nynorsk)', flag: '🇳🇴' },
  { code: Language.SV_SE, name: 'Svenska', flag: '🇸🇪' },
  { code: Language.DA_DK, name: 'Dansk', flag: '🇩🇰' },
  { code: Language.FI_FI, name: 'Suomi', flag: '🇫🇮' },
  { code: Language.DE_DE, name: 'Deutsch', flag: '🇩🇪' },
]

// Translation hook
export const useTranslation = () => {
  const [language, setLanguageState] = React.useState<Language>(() => {
    return (localStorage.getItem('language') as Language) || Language.EN_US
  })

  const setLanguage = (lang: Language) => {
    localStorage.setItem('language', lang)
    setLanguageState(lang)
  }

  const t = (key: string, params?: Record<string, any>): string => {
    let translation = translations[key]?.[language] || translations[key]?.[Language.EN_US] || key

    if (params) {
      Object.keys(params).forEach(paramKey => {
        translation = translation.replace(`{${paramKey}}`, params[paramKey])
      })
    }

    return translation
  }

  return { t, language, setLanguage }
}

// React import for hook
import React from 'react'
