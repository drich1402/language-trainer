import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth endpoints
  async register(email, password) {
    const response = await api.post('/api/auth/register', { email, password })
    return response.data
  },

  async login(email, password) {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  // Vocabulary endpoints
  async getNextReview() {
    const response = await api.get('/api/vocab/next-review')
    return response.data
  },

  async submitReview(vocabId, selectedVocabId, responseTimeMs) {
    const response = await api.post(`/api/vocab/${vocabId}/review`, {
      selected_vocab_id: selectedVocabId,
      response_time_ms: responseTimeMs,
    })
    return response.data
  },

  async getStats() {
    const response = await api.get('/api/vocab/stats')
    return response.data
  },

  async listVocabulary(limit = 50, offset = 0) {
    const response = await api.get('/api/vocab/list', {
      params: { limit, offset },
    })
    return response.data
  },
}
