/**
 * GDPR-Compliant Cookie Consent Banner
 * Granular cookie consent for EU/EEA markets
 */
import React, { useState, useEffect } from 'react'
import { useTranslation } from '../i18n/translations'
import { X, Settings, Check } from 'lucide-react'

interface ConsentPreferences {
  necessary: boolean
  functional: boolean
  analytics: boolean
  marketing: boolean
  performance: boolean
  timestamp: string
}

interface CookieConsentProps {
  onConsentChange?: (preferences: ConsentPreferences) => void
}

const CONSENT_COOKIE_NAME = 'cookie_consent'
const CONSENT_VALID_DAYS = 365

export const CookieConsent: React.FC<CookieConsentProps> = ({ onConsentChange }) => {
  const { t, language } = useTranslation()
  const [showBanner, setShowBanner] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [preferences, setPreferences] = useState<ConsentPreferences>({
    necessary: true, // Always true, cannot be disabled
    functional: false,
    analytics: false,
    marketing: false,
    performance: false,
    timestamp: new Date().toISOString()
  })

  // Check if consent already given
  useEffect(() => {
    const existingConsent = getCookie(CONSENT_COOKIE_NAME)
    if (!existingConsent) {
      setShowBanner(true)
    } else {
      try {
        const parsed = JSON.parse(existingConsent)
        const consentDate = new Date(parsed.timestamp)
        const daysSinceConsent = (Date.now() - consentDate.getTime()) / (1000 * 60 * 60 * 24)

        if (daysSinceConsent >= CONSENT_VALID_DAYS) {
          // Consent expired, show banner again
          setShowBanner(true)
        } else {
          // Valid consent exists
          setPreferences(parsed)
          onConsentChange?.(parsed)
        }
      } catch {
        setShowBanner(true)
      }
    }
  }, [onConsentChange])

  const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null
    return null
  }

  const setCookie = (name: string, value: string, days: number) => {
    const expires = new Date()
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000)
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`
  }

  const savePreferences = (prefs: ConsentPreferences) => {
    const prefsWithTimestamp = {
      ...prefs,
      timestamp: new Date().toISOString()
    }

    setCookie(CONSENT_COOKIE_NAME, JSON.stringify(prefsWithTimestamp), CONSENT_VALID_DAYS)
    setPreferences(prefsWithTimestamp)
    setShowBanner(false)
    setShowSettings(false)

    onConsentChange?.(prefsWithTimestamp)

    // Load third-party scripts based on consent
    loadThirdPartyScripts(prefsWithTimestamp)
  }

  const handleAcceptAll = () => {
    savePreferences({
      necessary: true,
      functional: true,
      analytics: true,
      marketing: true,
      performance: true,
      timestamp: new Date().toISOString()
    })
  }

  const handleRejectAll = () => {
    savePreferences({
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
      performance: false,
      timestamp: new Date().toISOString()
    })
  }

  const handleSaveCustom = () => {
    savePreferences(preferences)
  }

  const loadThirdPartyScripts = (prefs: ConsentPreferences) => {
    // Google Analytics
    if (prefs.analytics && !window.gtag) {
      const script = document.createElement('script')
      script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID'
      script.async = true
      document.head.appendChild(script)

      script.onload = () => {
        window.dataLayer = window.dataLayer || []
        function gtag(...args: any[]) {
          window.dataLayer.push(args)
        }
        window.gtag = gtag
        gtag('js', new Date())
        gtag('config', 'GA_MEASUREMENT_ID', {
          anonymize_ip: true,
          cookie_flags: 'SameSite=Strict;Secure'
        })
      }
    }

    // Facebook Pixel
    if (prefs.marketing && !window.fbq) {
      const script = document.createElement('script')
      script.innerHTML = `
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', 'YOUR_PIXEL_ID');
        fbq('track', 'PageView');
      `
      document.head.appendChild(script)
    }

    // Sentry Error Tracking
    if (prefs.performance && !window.Sentry) {
      const script = document.createElement('script')
      script.src = 'https://js.sentry-cdn.com/YOUR_DSN.min.js'
      script.crossOrigin = 'anonymous'
      document.head.appendChild(script)
    }
  }

  const togglePreference = (key: keyof Omit<ConsentPreferences, 'necessary' | 'timestamp'>) => {
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  if (!showBanner) return null

  return (
    <>
      {/* Cookie Banner */}
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 shadow-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          {!showSettings ? (
            // Simple Banner
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {t('cookie.title')}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('cookie.description')}
                  {' '}
                  <a href="/privacy-policy" className="text-blue-600 hover:underline">
                    {t('cookie.learn_more')}
                  </a>
                </p>
              </div>

              <div className="flex flex-wrap gap-2 sm:flex-nowrap">
                <button
                  onClick={handleRejectAll}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  {t('cookie.reject_all')}
                </button>
                <button
                  onClick={() => setShowSettings(true)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors flex items-center gap-2"
                >
                  <Settings className="w-4 h-4" />
                  {t('cookie.customize')}
                </button>
                <button
                  onClick={handleAcceptAll}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  {t('cookie.accept_all')}
                </button>
              </div>
            </div>
          ) : (
            // Detailed Settings
            <div className="max-h-[80vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                  {t('cookie.customize_title')}
                </h3>
                <button
                  onClick={() => setShowSettings(false)}
                  className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                {/* Necessary Cookies - Always On */}
                <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Check className="w-5 h-5 text-green-600" />
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        {t('cookie.necessary_title')}
                      </h4>
                    </div>
                    <span className="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded">
                      {t('cookie.always_active')}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {t('cookie.necessary_description')}
                  </p>
                </div>

                {/* Functional Cookies */}
                <CookieCategory
                  title={t('cookie.functional_title')}
                  description={t('cookie.functional_description')}
                  enabled={preferences.functional}
                  onToggle={() => togglePreference('functional')}
                />

                {/* Analytics Cookies */}
                <CookieCategory
                  title={t('cookie.analytics_title')}
                  description={t('cookie.analytics_description')}
                  enabled={preferences.analytics}
                  onToggle={() => togglePreference('analytics')}
                />

                {/* Marketing Cookies */}
                <CookieCategory
                  title={t('cookie.marketing_title')}
                  description={t('cookie.marketing_description')}
                  enabled={preferences.marketing}
                  onToggle={() => togglePreference('marketing')}
                />

                {/* Performance Cookies */}
                <CookieCategory
                  title={t('cookie.performance_title')}
                  description={t('cookie.performance_description')}
                  enabled={preferences.performance}
                  onToggle={() => togglePreference('performance')}
                />
              </div>

              <div className="flex gap-2 mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={handleRejectAll}
                  className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  {t('cookie.reject_all')}
                </button>
                <button
                  onClick={handleSaveCustom}
                  className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  {t('cookie.save_preferences')}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

interface CookieCategoryProps {
  title: string
  description: string
  enabled: boolean
  onToggle: () => void
}

const CookieCategory: React.FC<CookieCategoryProps> = ({
  title,
  description,
  enabled,
  onToggle
}) => {
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-gray-900 dark:text-white">{title}</h4>
        <button
          onClick={onToggle}
          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
            enabled ? 'bg-blue-600' : 'bg-gray-300'
          }`}
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
              enabled ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  )
}

// TypeScript declarations for third-party scripts
declare global {
  interface Window {
    gtag?: (...args: any[]) => void
    dataLayer?: any[]
    fbq?: (...args: any[]) => void
    _fbq?: any
    Sentry?: any
  }
}

export default CookieConsent
