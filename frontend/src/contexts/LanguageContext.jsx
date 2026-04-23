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

const baseTranslations = {
  summary: 'Summary',
  eligibility: 'Eligibility',
  benefits: 'Benefits',
  process: 'Application Process',
  explainSimpler: 'Explain Simpler',
  showStandard: 'Show Standard Explanation',
  search: 'Search',
  compare: 'Compare',
  checkEligibility: 'Check Eligibility',
  home: 'Home',
  explore: 'Explore',
  allSchemes: 'All Schemes',
  searchSchemes: 'Search schemes...',
  instantSearch: 'Instant Search',
  multilingual: 'Multilingual',
  findScheme: 'Find any government scheme in seconds',
  availableLanguages: 'Available in 6 Indian languages',
  findQualify: 'Find schemes you qualify for',
  understandSchemes: 'Understand Government Schemes Instantly',
  clearExplanations: 'Get clear, simple explanations in your language. Check eligibility. Compare schemes.',
  enterScheme: 'Enter a scheme name (e.g., PMAY, PM-KISAN)',
  exploreSchemes: 'Explore Schemes',
  browseSchemes: 'Browse all available government schemes',
  found: 'Found',
  schemes: 'schemes',
  noSchemes: 'No schemes found matching your criteria',
  clearFilters: 'Clear Filters',
  compareSchemes: 'Compare Schemes',
  compareSideBySide: 'Compare two government schemes side by side',
  firstScheme: 'First Scheme',
  secondScheme: 'Second Scheme',
  selectScheme: 'Select a scheme',
  checkYourEligibility: 'Check Your Eligibility',
  findQualifyFor: 'Find out which government schemes you qualify for',
  age: 'Age',
  income: 'Annual Income (₹)',
  gender: 'Gender',
  category: 'Category',
  state: 'State',
  occupation: 'Occupation',
  checking: 'Checking...',
  eligibleSchemes: 'Eligible Schemes',
  notEligible: 'Not Eligible',
  whyNotEligible: 'Why not eligible:',
  documents: 'Documents',
  visitWebsite: 'Visit Website',
  aspect: 'Aspect',
  description: 'Description',
  documentsRequired: 'Documents Required',
  officialWebsite: 'Official Website',
  schemeExplainer: 'Scheme Explainer'
}

export const TRANSLATIONS = {
  en: baseTranslations,
  hi: {
    summary: 'सारांश',
    eligibility: 'पात्रता',
    benefits: 'लाभ',
    process: 'आवेदन प्रक्रिया',
    explainSimpler: 'सरल समझाएं',
    showStandard: 'मानक स्पष्टीकरण दिखाएं',
    search: 'खोजें',
    compare: 'तुलना करें',
    checkEligibility: 'पात्रता जांचें',
    home: 'होम',
    explore: 'खोजें',
    allSchemes: 'सभी योजनाएं',
    searchSchemes: 'योजनाएं खोजें...',
    instantSearch: 'तत्काल खोज',
    multilingual: 'बहुभाषी',
    findScheme: 'सेकंडों में कोई भी सरकारी योजना खोजें',
    availableLanguages: '6 भारतीय भाषाओं में उपलब्ध',
    findQualify: 'जानें आप किन योजनाओं के लिए योग्य हैं',
    understandSchemes: 'सरकारी योजनाओं को तुरंत समझें',
    clearExplanations: 'अपनी भाषा में स्पष्ट, सरल स्पष्टीकरण प्राप्त करें। पात्रता जांचें। योजनाओं की तुलना करें।',
    enterScheme: 'योजना का नाम दर्ज करें (जैसे, PMAY, PM-KISAN)',
    exploreSchemes: 'योजनाएं खोजें',
    browseSchemes: 'सभी उपलब्ध सरकारी योजनाओं को ब्राउज़ करें',
    found: 'मिला',
    schemes: 'योजनाएं',
    noSchemes: 'आपके मानदंडों से मेल खाने वाली कोई योजना नहीं मिली',
    clearFilters: 'फ़िल्टर साफ़ करें',
    compareSchemes: 'योजनाओं की तुलना करें',
    compareSideBySide: 'दो सरकारी योजनाओं की साथ-साथ तुलना करें',
    firstScheme: 'पहली योजना',
    secondScheme: 'दूसरी योजना',
    selectScheme: 'एक योजना चुनें',
    checkYourEligibility: 'अपनी पात्रता जांचें',
    findQualifyFor: 'जानें आप किन सरकारी योजनाओं के लिए योग्य हैं',
    age: 'आयु',
    income: 'वार्षिक आय (₹)',
    gender: 'लिंग',
    category: 'श्रेणी',
    state: 'राज्य',
    occupation: 'व्यवसाय',
    checking: 'जांच रहे हैं...',
    eligibleSchemes: 'योग्य योजनाएं',
    notEligible: 'योग्य नहीं',
    whyNotEligible: 'योग्य क्यों नहीं:',
    documents: 'दस्तावेज़',
    visitWebsite: 'वेबसाइट पर जाएं',
    aspect: 'पहलू',
    description: 'विवरण',
    documentsRequired: 'आवश्यक दस्तावेज़',
    officialWebsite: 'आधिकारिक वेबसाइट',
    schemeExplainer: 'योजना व्याख्याकार'
  },
  te: baseTranslations,
  ta: baseTranslations,
  kn: baseTranslations,
  bn: baseTranslations
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
