import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const getAllSchemes = async () => {
  const response = await axios.get(`${API_URL}/api/schemes`)
  return response.data
}

export const getScheme = async (name) => {
  const response = await axios.get(`${API_URL}/api/scheme/${encodeURIComponent(name)}`)
  return response.data
}

export const explainScheme = async (schemeName, simplificationLevel = 'standard', language = 'en') => {
  const response = await axios.post(`${API_URL}/api/explain`, {
    scheme_name: schemeName,
    simplification_level: simplificationLevel,
    language
  })
  return response.data
}

export const checkEligibility = async (userDetails) => {
  const response = await axios.post(`${API_URL}/api/check-eligibility`, userDetails)
  return response.data
}

export const compareSchemes = async (scheme1, scheme2) => {
  const response = await axios.post(`${API_URL}/api/compare`, { scheme1, scheme2 })
  return response.data
}
