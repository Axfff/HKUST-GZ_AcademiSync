<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Create an Account</h2>
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            id="name"
            v-model="name"
            type="text"
            required
            class="form-input"
            placeholder="Enter your name"
          />
        </div>
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
            placeholder="Choose a password"
          />
        </div>
        <button type="submit" class="auth-button">Register</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p class="auth-link">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useAuthStore } from '../../store/auth'
import { hashPassword } from '../../utils/crypto'
import type { ApiError } from '../../types/api'

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const errorMessage = ref('')
    const authStore = useAuthStore()

    const handleRegister = async () => {
      try {
        const hashedPassword = await hashPassword(password.value)
        await authStore.register(email.value, hashedPassword, name.value)
      } catch (error) {
        const apiError = error as ApiError
        errorMessage.value = apiError.response?.data?.message || 'Registration failed'
      }
    }

    return { name, email, password, handleRegister, errorMessage }
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
</style>
