import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, FileText } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import Skeleton from '../components/Skeleton'
import { checkEligibility } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'

const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Puducherry'
]

export default function Eligibility() {
  const navigate = useNavigate()
  const { t } = useLanguage()
  const [formData, setFormData] = useState({
    age: '',
    income: '',
    gender: 'Male',
    category: 'General',
    state: 'Delhi',
    occupation: 'Salaried'
  })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const data = await checkEligibility({
        age: parseInt(formData.age),
        income: parseInt(formData.income),
        gender: formData.gender,
        category: formData.category,
        state: formData.state,
        occupation: formData.occupation
      })
      setResults(data)
    } catch (err) {
      console.error('Eligibility check failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-[#1E293B] mb-4">{t('checkYourEligibility')}</h1>
        <p className="text-muted">{t('findQualifyFor')}</p>
      </div>

      <Card className="max-w-2xl mx-auto mb-12">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('age')}</label>
              <Input
                type="number"
                value={formData.age}
                onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                placeholder={t('age')}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('income')}</label>
              <Input
                type="number"
                value={formData.income}
                onChange={(e) => setFormData({ ...formData, income: e.target.value })}
                placeholder={t('income')}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('gender')}</label>
              <select
                value={formData.gender}
                onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('category')}</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <option>General</option>
                <option>OBC</option>
                <option>SC</option>
                <option>ST</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('state')}</label>
              <select
                value={formData.state}
                onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                {INDIAN_STATES.map(state => (
                  <option key={state}>{state}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-[#1E293B] mb-2">{t('occupation')}</label>
              <select
                value={formData.occupation}
                onChange={(e) => setFormData({ ...formData, occupation: e.target.value })}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <option>Farmer</option>
                <option>Student</option>
                <option>Salaried</option>
                <option>Self-employed</option>
                <option>Unemployed</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? t('checking') : t('checkEligibility')}
          </Button>
        </form>
      </Card>

      {loading && (
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <Card key={i}>
              <Skeleton className="h-6 w-2/3 mb-2" />
              <Skeleton className="h-4 w-full" />
            </Card>
          ))}
        </div>
      )}

      {results && !loading && (
        <div className="space-y-8">
          {results.eligible.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold text-[#1E293B] mb-4 flex items-center">
                <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
                {t('eligibleSchemes')} ({results.total_eligible})
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.eligible.map((scheme) => (
                  <Card
                    key={scheme.name}
                    className="cursor-pointer hover:shadow-lg hover:border-green-500 transition-all border-2 border-green-200"
                    onClick={() => navigate('/results', { state: { schemeName: scheme.name } })}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-lg font-semibold text-[#1E293B] flex-1">{scheme.name}</h3>
                      <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                    </div>
                    <p className="text-sm text-muted mb-3">{scheme.description}</p>
                    <div className="text-sm text-[#1E293B] mb-2">
                      <strong>{t('benefits')}:</strong> {scheme.benefits}
                    </div>
                    {scheme.documents.length > 0 && (
                      <div className="text-sm text-muted">
                        <strong>{t('documents')}:</strong> {scheme.documents.join(', ')}
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </div>
          )}

          {results.not_eligible.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold text-[#1E293B] mb-4 flex items-center">
                <XCircle className="w-6 h-6 text-red-500 mr-2" />
                {t('notEligible')} ({results.not_eligible.length})
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.not_eligible.map((scheme) => (
                  <Card key={scheme.name} className="border-2 border-red-100">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-lg font-semibold text-[#1E293B] flex-1">{scheme.name}</h3>
                      <XCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                    </div>
                    <p className="text-sm text-muted mb-3">{scheme.description}</p>
                    {scheme.reasons.length > 0 && (
                      <div className="text-sm text-red-600">
                        <strong>{t('whyNotEligible')}</strong>
                        <ul className="list-disc list-inside mt-1">
                          {scheme.reasons.map((reason, i) => (
                            <li key={i}>{reason}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
