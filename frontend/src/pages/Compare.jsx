import { useState, useEffect } from 'react'
import { ArrowRight } from 'lucide-react'
import Input from '../components/Input'
import Button from '../components/Button'
import Card from '../components/Card'
import Skeleton from '../components/Skeleton'
import { getAllSchemes, compareSchemes } from '../services/api'

export default function Compare() {
  const [schemes, setSchemes] = useState([])
  const [scheme1, setScheme1] = useState('')
  const [scheme2, setScheme2] = useState('')
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadSchemes()
  }, [])

  const loadSchemes = async () => {
    try {
      const data = await getAllSchemes()
      setSchemes(data.schemes)
    } catch (err) {
      console.error('Failed to load schemes:', err)
    }
  }

  const handleCompare = async () => {
    if (!scheme1 || !scheme2) return
    
    setLoading(true)
    try {
      const result = await compareSchemes(scheme1, scheme2)
      setComparison(result)
    } catch (err) {
      console.error('Comparison failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-[#1E293B] mb-4">Compare Schemes</h1>
        <p className="text-muted">Compare two government schemes side by side</p>
      </div>

      <div className="max-w-4xl mx-auto mb-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
          <div>
            <label className="block text-sm font-medium text-[#1E293B] mb-2">First Scheme</label>
            <select
              value={scheme1}
              onChange={(e) => setScheme1(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option value="">Select a scheme</option>
              {schemes.map((s) => (
                <option key={s.name} value={s.name}>{s.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-[#1E293B] mb-2">Second Scheme</label>
            <select
              value={scheme2}
              onChange={(e) => setScheme2(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option value="">Select a scheme</option>
              {schemes.map((s) => (
                <option key={s.name} value={s.name}>{s.name}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex justify-center mt-6">
          <Button onClick={handleCompare} disabled={loading || !scheme1 || !scheme2}>
            <ArrowRight className="w-5 h-5 mr-2" />
            Compare
          </Button>
        </div>
      </div>

      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2].map((i) => (
            <div key={i} className="space-y-4">
              <Skeleton className="h-8 w-2/3" />
              <Card>
                <Skeleton className="h-6 w-1/3 mb-4" />
                <Skeleton className="h-4 w-full mb-2" />
                <Skeleton className="h-4 w-5/6" />
              </Card>
            </div>
          ))}
        </div>
      )}

      {!loading && comparison && (
        <div>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 px-4 py-3 text-left font-semibold text-[#1E293B]">Aspect</th>
                  <th className="border border-gray-200 px-4 py-3 text-left font-semibold text-[#1E293B]">{comparison.scheme1.name}</th>
                  <th className="border border-gray-200 px-4 py-3 text-left font-semibold text-[#1E293B]">{comparison.scheme2.name}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 px-4 py-3 font-medium text-[#1E293B]">Description</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme1.description}</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme2.description}</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 px-4 py-3 font-medium text-[#1E293B]">Eligibility</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme1.eligibility}</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme2.eligibility}</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 px-4 py-3 font-medium text-[#1E293B]">Benefits</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme1.benefits}</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme2.benefits}</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 px-4 py-3 font-medium text-[#1E293B]">Documents Required</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme1.documents.join(', ')}</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">{comparison.scheme2.documents.join(', ')}</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 px-4 py-3 font-medium text-[#1E293B]">Official Website</td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">
                    <a href={comparison.scheme1.url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                      Visit Website
                    </a>
                  </td>
                  <td className="border border-gray-200 px-4 py-3 text-sm">
                    <a href={comparison.scheme2.url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                      Visit Website
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
