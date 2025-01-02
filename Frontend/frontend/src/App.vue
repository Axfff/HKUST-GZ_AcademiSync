<template>
  <div id="app">
    <header>
      <nav class="navbar">
        <div class="nav-container">
          <div class="logo">
            <router-link to="/">AcademiSync</router-link>
          </div>
          <ul class="nav-links">
            <li v-if="!authStore.isAuthenticated">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li v-if="!authStore.isAuthenticated">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li v-if="authStore.isAuthenticated">
              <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
            </li>
            <li v-if="authStore.isAuthenticated">
              <button class="nav-button" @click="authStore.logout">Logout</button>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="site-footer">
      <div class="nav-container">
        <p>&copy; 2024 AcademiSync. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useAuthStore } from './store/auth' // Adjust the path to your store

export default defineComponent({
  name: 'App',
  setup() {
    const authStore = useAuthStore() // Pinia store for authentication
    return { authStore }
  },
})
</script>

<style scoped>
.navbar {
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  padding: 1rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  color: var(--color-heading);
  font-size: 1.5rem;
  font-weight: 600;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: var(--color-text);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: var(--color-background-mute);
}

.nav-button {
  background-color: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-button:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.main-content {
  min-height: calc(100vh - 120px);
}

.site-footer {
  background-color: var(--color-background);
  border-top: 1px solid var(--color-border);
  padding: 1.5rem 0;
  color: var(--color-text-light-2);
}
</style>
