import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Filter } from 'lucide-react'
import Card from '../components/Card'
import Input from '../components/Input'
import Button from '../components/Button'
import Skeleton from '../components/Skeleton'
import { useLanguage } from '../contexts/LanguageContext'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'

export default function Explore() {
  const [schemes, setSchemes] = useState([])
  const [filteredSchemes, setFilteredSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const navigate = useNavigate()
  const { t } = useLanguage()

  const categories = [
    { id: 'all', label: 'All Schemes' },
    { id: 'farmer', label: 'Farmers' },
    { id: 'student', label: 'Students' },
    { id: 'woman', label: 'Women' },
    { id: 'general', label: 'General' }
  ]

  useEffect(() => {
    fetchSchemes()
  }, [])

  useEffect(() => {
    filterSchemes()
  }, [searchQuery, selectedCategory, schemes])

  const fetchSchemes = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/search.js`)
      setSchemes(response.data.schemes || [])
    } catch (error) {
      console.error('Failed to fetch schemes:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterSchemes = () => {
    let results = schemes

    if (selectedCategory !== 'all') {
      results = results.filter(s => s.target === selectedCategory)
    }

    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      results = results.filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.description.toLowerCase().includes(query)
      )
    }

    setFilteredSchemes(results)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-[#1E293B] mb-4">{t('exploreSchemes')}</h1>
        <p className="text-muted">{t('browseSchemes')}</p>
      </div>

      <div className="mb-8">
        <div className="flex gap-3 mb-6">
          <Input
            placeholder={t('searchSchemes')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1"
          />
          <Button onClick={filterSchemes} className="flex items-center space-x-2">
            <Search className="w-5 h-5" />
            <span>{t('search')}</span>
          </Button>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <Filter className="w-5 h-5 text-muted" />
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                selectedCategory === cat.id
                  ? 'bg-primary text-white'
                  : 'bg-white border border-gray-300 text-[#1E293B] hover:border-primary'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i}>
              <Skeleton className="h-6 w-2/3 mb-3" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-5/6" />
            </Card>
          ))}
        </div>
      ) : (
        <>
          <div className="mb-4 text-muted">
            {t('found')} {filteredSchemes.length} {t('schemes')}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSchemes.map((scheme) => (
              <Card
                key={scheme.name}
                className="cursor-pointer hover:shadow-lg hover:border-primary transition-all"
                onClick={() => navigate('/results', { state: { schemeName: scheme.name } })}
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold text-[#1E293B] flex-1">{scheme.name}</h3>
                  <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full capitalize">
                    {scheme.target}
                  </span>
                </div>
                <p className="text-sm text-muted line-clamp-2">{scheme.description}</p>
              </Card>
            ))}
          </div>
        </>
      )}

      {!loading && filteredSchemes.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted text-lg">{t('noSchemes')}</p>
          <Button
            onClick={() => {
              setSearchQuery('')
              setSelectedCategory('all')
            }}
            variant="secondary"
            className="mt-4"
          >
            {t('clearFilters')}
          </Button>
        </div>
      )}
    </div>
  )
}
