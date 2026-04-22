import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Sparkles } from 'lucide-react'
import Input from '../components/Input'
import Button from '../components/Button'
import Card from '../components/Card'
import { getAllSchemes } from '../services/api'

export default function Home() {
  const [schemeName, setSchemeName] = useState('')
  const [allSchemes, setAllSchemes] = useState([])
  const [filteredSchemes, setFilteredSchemes] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadSchemes()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = allSchemes.filter(s =>
        s.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredSchemes(filtered)
    } else {
      setFilteredSchemes(allSchemes.slice(0, 8))
    }
  }, [searchQuery, allSchemes])

  const loadSchemes = async () => {
    try {
      const data = await getAllSchemes()
      setAllSchemes(data.schemes)
      setFilteredSchemes(data.schemes.slice(0, 8))
    } catch (err) {
      console.error('Failed to load schemes:', err)
    }
  }

  const handleSearch = () => {
    if (schemeName.trim()) {
      navigate('/results', { state: { schemeName } })
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-16">
        <div className="inline-flex items-center space-x-2 bg-primary/10 px-4 py-2 rounded-full mb-6">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium text-primary">AI-Powered Multilingual Assistant</span>
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold text-[#1E293B] mb-6 leading-tight">
          Understand Government<br />Schemes Instantly
        </h1>
        
        <p className="text-xl text-muted max-w-2xl mx-auto mb-12">
          Get clear, simple explanations in your language. Check eligibility. Compare schemes.
        </p>

        <div className="max-w-2xl mx-auto">
          <div className="flex gap-3">
            <Input
              placeholder="Enter a scheme name (e.g., PMAY, PM-KISAN)"
              value={schemeName}
              onChange={(e) => setSchemeName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Button onClick={handleSearch} className="flex items-center space-x-2">
              <Search className="w-5 h-5" />
              <span>Search</span>
            </Button>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-[#1E293B]">All Schemes</h2>
          <Input
            placeholder="Search schemes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="max-w-xs"
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {filteredSchemes.map((scheme) => (
            <Card
              key={scheme.name}
              className="cursor-pointer hover:border-primary hover:shadow-lg transition-all"
              onClick={() => navigate('/results', { state: { schemeName: scheme.name } })}
            >
              <h3 className="font-medium text-[#1E293B] text-sm mb-2">{scheme.name}</h3>
              <p className="text-xs text-muted line-clamp-2">{scheme.description}</p>
            </Card>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
        <Card>
          <div className="text-center">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Search className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-[#1E293B] mb-2">Instant Search</h3>
            <p className="text-muted text-sm">Find any government scheme in seconds</p>
          </div>
        </Card>

        <Card>
          <div className="text-center">
            <div className="w-12 h-12 bg-accent/20 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-6 h-6 text-accent" />
            </div>
            <h3 className="text-lg font-semibold text-[#1E293B] mb-2">Multilingual</h3>
            <p className="text-muted text-sm">Available in 6 Indian languages</p>
          </div>
        </Card>

        <Card>
          <div className="text-center">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-[#1E293B] mb-2">Check Eligibility</h3>
            <p className="text-muted text-sm">Find schemes you qualify for</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
