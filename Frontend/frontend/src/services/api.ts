import axios from 'axios'
import { useAuthStore } from '../store/auth'
import router from '../router'

const api = axios.create({
  baseURL:
    process.env.NODE_ENV === 'production'
      ? 'https://courseComment.hkust-gz.Axfff.com/v1/api'
      : 'http://localhost:3000/v1/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config,
    })

    // Handle token expiration
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      router.push({
        path: '/login',
        query: { redirect: router.currentRoute.value.fullPath },
      })
    }

    return Promise.reject(error)
  },
)

// Add a request interceptor to include the token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

export default api
