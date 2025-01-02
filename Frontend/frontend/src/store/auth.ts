import { defineStore } from 'pinia'
import api from '../services/api'
import router from '../router'

interface User {
  id: number
  email: string
  name: string
  created_at: string
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),

  actions: {
    async login(email: string, password_hash: string) {
      try {
        const response = await api.post('/auth/login', {
          email,
          password_hash,
        })

        const { token, user } = response.data
        this.token = token
        this.user = user
        this.isAuthenticated = true
        localStorage.setItem('token', token)

        await router.push('/dashboard')
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    async register(email: string, password_hash: string, name: string) {
      try {
        const response = await api.post('/auth/register', {
          email,
          password_hash,
          name,
        })

        const { token, user } = response.data
        this.token = token
        this.user = user
        this.isAuthenticated = true
        localStorage.setItem('token', token)

        await router.push('/dashboard')
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      router.push('/login')
    },
  },
})
