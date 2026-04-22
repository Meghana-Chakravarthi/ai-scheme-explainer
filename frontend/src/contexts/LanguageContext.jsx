import { createContext, useContext, useState } from 'react'

const LanguageContext = createContext()

export const LANGUAGES = {
  en: { name: 'English', code: 'en' },
  hi: { name: 'हिंदी', code: 'hi' },
  te: { name: 'తెలుగు', code: 'te' },
  ta: { name: 'தமிழ்', code: 'ta' },
  kn: { name: 'ಕನ್ನಡ', code: 'kn' },
  bn: { name: 'বাংলা', code: 'bn' }
}

export const TRANSLATIONS = {
  en: {
    summary: 'Summary',
    eligibility: 'Eligibility',
    benefits: 'Benefits',
    process: 'Application Process',
    explainSimpler: 'Explain Simpler',
    showStandard: 'Show Standard Explanation',
    search: 'Search',
    compare: 'Compare',
    checkEligibility: 'Check Eligibility'
  },
  hi: {
    summary: 'सारांश',
    eligibility: 'पात्रता',
    benefits: 'लाभ',
    process: 'आवेदन प्रक्रिया',
    explainSimpler: 'सरल समझाएं',
    showStandard: 'मानक स्पष्टीकरण दिखाएं',
    search: 'खोजें',
    compare: 'तुलना करें',
    checkEligibility: 'पात्रता जांचें'
  }
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en')

  const t = (key) => {
    return TRANSLATIONS[language]?.[key] || TRANSLATIONS.en[key] || key
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider')
  }
  return context
}
