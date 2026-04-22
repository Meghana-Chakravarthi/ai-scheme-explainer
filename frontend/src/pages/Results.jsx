import { useState, useEffect } from 'react'
import { useLocation, useParams } from 'react-router-dom'
import { CheckCircle, Users, Gift, FileText, Copy, RefreshCw } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import Skeleton from '../components/Skeleton'
import { explainScheme } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'

export default function Results() {
  const location = useLocation()
  const params = useParams()
  const { language, t } = useLanguage()
  const schemeName = params.name || location.state?.schemeName
  
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)
  const [isSimplified, setIsSimplified] = useState(false)

  useEffect(() => {
    if (schemeName) {
      fetchSchemeData('standard')
    }
  }, [schemeName, language])

  const fetchSchemeData = async (level) => {
    setLoading(true)
    setError(null)
    try {
      const result = await explainScheme(schemeName, level, language)
      setData(result)
      setIsSimplified(level === 'simple')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch scheme details. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const toggleSimplification = () => {
    const newLevel = isSimplified ? 'standard' : 'simple'
    fetchSchemeData(newLevel)
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (!schemeName) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
        <p className="text-muted">No scheme selected. Please search for a scheme.</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Skeleton className="h-12 w-2/3 mb-8" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <Skeleton className="h-6 w-1/3 mb-4" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-5/6" />
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={() => fetchSchemeData('standard')} variant="secondary">
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </div>
      </div>
    )
  }

  const sections = [
    { title: t('summary'), icon: FileText, content: data.summary },
    { title: t('eligibility'), icon: Users, content: data.eligibility },
    { title: t('benefits'), icon: Gift, content: data.benefits },
    { title: t('process'), icon: CheckCircle, content: data.process }
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {copied && (
        <div className="fixed top-20 right-4 bg-primary text-white px-4 py-2 rounded-lg shadow-lg z-50">
          Copied to clipboard!
        </div>
      )}
      
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-[#1E293B] mb-2">{data.scheme_name || schemeName}</h1>
        <p className="text-muted">AI-generated explanation</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sections.map(({ title, icon: Icon, content }) => (
          <Card key={title} className="group">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                  <Icon className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-[#1E293B]">{title}</h2>
              </div>
              <button
                onClick={() => copyToClipboard(content)}
                className="opacity-0 group-hover:opacity-100 transition-opacity p-2 hover:bg-gray-100 rounded"
              >
                <Copy className="w-4 h-4 text-muted" />
              </button>
            </div>
            <p className="text-[#1E293B] leading-relaxed">{content}</p>
          </Card>
        ))}
      </div>

      <div className="mt-8 flex justify-center">
        <Button onClick={toggleSimplification} variant="secondary" disabled={loading}>
          <RefreshCw className="w-4 h-4 mr-2" />
          {isSimplified ? t('showStandard') : t('explainSimpler')}
        </Button>
      </div>
    </div>
  )
}
