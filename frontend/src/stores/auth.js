import api from '@/services/api'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('access_token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async register(email, password) {
      try {
        const data = await api.register(email, password)
        this.setAuth(data)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Registration failed',
        }
      }
    },

    async login(email, password) {
      try {
        const data = await api.login(email, password)
        this.setAuth(data)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Login failed',
        }
      }
    },

    setAuth(data) {
      this.token = data.access_token
      this.user = data.user
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    },
  },
})
