import { Link } from 'react-router-dom'
import { FileText, User, Globe } from 'lucide-react'
import { useLanguage, LANGUAGES } from '../contexts/LanguageContext'

export default function Navbar() {
  const { language, setLanguage, t } = useLanguage()

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2">
              <FileText className="w-6 h-6 text-primary" />
              <span className="text-xl font-semibold text-[#1E293B]">{t('schemeExplainer')}</span>
            </Link>
            <div className="hidden md:flex space-x-6">
              <Link to="/" className="text-muted hover:text-[#1E293B] transition-colors">{t('home')}</Link>
              <Link to="/explore" className="text-muted hover:text-[#1E293B] transition-colors">{t('explore')}</Link>
              <Link to="/eligibility" className="text-muted hover:text-[#1E293B] transition-colors">{t('checkEligibility')}</Link>
              <Link to="/compare" className="text-muted hover:text-[#1E293B] transition-colors">{t('compare')}</Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Globe className="w-5 h-5 text-muted absolute left-3 top-1/2 -translate-y-1/2" />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="pl-10 pr-4 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white"
              >
                {Object.entries(LANGUAGES).map(([code, { name }]) => (
                  <option key={code} value={code}>{name}</option>
                ))}
              </select>
            </div>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
