<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Login to AcademiSync</h2>
      <p v-if="sessionExpired" class="session-expired">
        Your session has expired. Please login again.
      </p>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="form-input"
            placeholder="Enter your email"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="form-input"
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" class="auth-button">Login</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p class="auth-link">
          Don't have an account?
          <router-link to="/register">Register here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useAuthStore } from '../../store/auth'
import { useRoute, useRouter } from 'vue-router'
import { hashPassword } from '../../utils/crypto'
import type { ApiError } from '../../types/api'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const email = ref('')
    const password = ref('')
    const errorMessage = ref('')
    const authStore = useAuthStore()
    const route = useRoute()
    const router = useRouter()

    const sessionExpired = computed(() => route.query.expired === 'true')

    const handleLogin = async () => {
      try {
        const hashedPassword = await hashPassword(password.value)
        await authStore.login(email.value, hashedPassword)

        // Redirect to the original page or dashboard
        const redirectPath = (route.query.redirect as string) || '/dashboard'
        router.push(redirectPath)
      } catch (error) {
        const apiError = error as ApiError
        errorMessage.value = apiError.response?.data?.message || 'Login failed'
      }
    }

    return { email, password, handleLogin, errorMessage, sessionExpired }
  },
})
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.auth-card {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.auth-title {
  color: var(--color-heading);
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: var(--color-text);
  font-size: 0.9rem;
  font-weight: 500;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
  background: var(--color-background);
  color: var(--color-text);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-border-hover);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.auth-button {
  background-color: #4a90e2;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.auth-button:hover {
  background-color: #357abd;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  text-align: center;
}

.auth-link {
  text-align: center;
  font-size: 0.9rem;
  color: var(--color-text-light-2);
}

.auth-link a {
  color: #4a90e2;
  text-decoration: none;
  font-weight: 500;
}

.auth-link a:hover {
  text-decoration: underline;
}

.session-expired {
  background-color: #fff3cd;
  color: #856404;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  text-align: center;
}
</style>
