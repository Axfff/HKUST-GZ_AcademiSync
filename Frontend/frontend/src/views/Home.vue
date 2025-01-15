<template>
  <div class="home page-container">
    <div class="search-section">
      <input
        v-model="searchQuery"
        @input="searchCourses"
        type="text"
        placeholder="Search courses..."
        class="search-input"
      />
      <div class="subject-filter">
        <button
          v-for="subject in subjects"
          :key="subject"
          @click="selectSubject(subject)"
          :class="['subject-button', { 'is-active': selectedSubject === subject }]"
        >
          {{ subject }}
        </button>
      </div>
    </div>

    <!-- Followed Courses Section -->
    <section class="courses-section">
      <h2 class="section-title">Followed Courses</h2>
      <div v-if="loadingFollowed" class="loading">Loading followed courses...</div>
      <div v-else-if="filteredFollowedCourses.length" class="grid-container">
        <div v-for="course in filteredFollowedCourses" :key="course.id" class="course-card">
          <router-link :to="`/courses/${course.id}`" class="course-content">
            <div class="course-header">
              <h3 class="course-title">{{ course.name }}</h3>
              <span class="course-code">{{ course.course_code }}</span>
            </div>
            <p class="course-description">{{ truncateDescription(course.description) }}</p>
          </router-link>
          <div class="card-footer">
            <FollowButton :course-id="course.id" @follow-updated="fetchFollowedCourses" />
          </div>
        </div>
      </div>
      <div v-else class="empty-state">You haven't followed any courses yet.</div>
    </section>

    <!-- All Courses Section -->
    <section class="courses-section">
      <h2 class="section-title">All Courses</h2>
      <div v-if="loading" class="loading">Loading courses...</div>
      <div v-else class="grid-container">
        <div v-for="course in filteredCourses" :key="course.id" class="course-card">
          <router-link :to="`/courses/${course.id}`" class="course-content">
            <div class="course-header">
              <h3 class="course-title">{{ course.name }}</h3>
              <span class="course-code">{{ course.course_code }}</span>
            </div>
            <p class="course-description">{{ truncateDescription(course.description) }}</p>
          </router-link>
          <div class="card-footer">
            <FollowButton :course-id="course.id" @follow-updated="fetchFollowedCourses" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import api from '../services/api'
import FollowButton from '../components/Follows/FollowButton.vue'
import { useAuthStore } from '../store/auth'

interface Course {
  id: number
  course_code: string
  name: string
  description: string
  created_at: string
}

export default defineComponent({
  name: 'HomeView',
  components: {
    FollowButton,
  },
  setup() {
    const courses = ref<Course[]>([])
    const followedCourses = ref<Course[]>([])
    const loading = ref(false)
    const loadingFollowed = ref(false)
    const searchQuery = ref('')
    const selectedSubject = ref('')
    const authStore = useAuthStore()

    const subjects = [
      'UCMP', 'UCUG', 'UFUG', 'UGOD', 'AIAA', 'AMAT', 'BSBE',
      'CMAA', 'DSAA', 'EOAS', 'FTEC', 'FUNH', 'INFH', 'INTR',
      'IOTA', 'IPEN', 'LANG', 'MICS', 'PDEV', 'PLED', 'ROAS',
      'SEEN', 'SMMG', 'SOCH', 'SYSH'
    ]

    const selectSubject = (subject: string) => {
      selectedSubject.value = selectedSubject.value === subject ? '' : subject
    }

    const filteredCourses = computed(() => {
      let filtered = courses.value
      if (selectedSubject.value) {
        filtered = filtered.filter(course =>
          course.course_code.startsWith(selectedSubject.value + ' ')
        )
      }
      return filtered
    })

    const filteredFollowedCourses = computed(() => {
      let filtered = followedCourses.value
      if (selectedSubject.value) {
        filtered = filtered.filter(course =>
          course.course_code.startsWith(selectedSubject.value + ' ')
        )
      }
      return filtered
    })

    const truncateDescription = (description: string) => {
      return description.length > 150 ? description.slice(0, 147) + '...' : description
    }

    const fetchFollowedCourses = async () => {
      if (!authStore.isAuthenticated) {
        followedCourses.value = []
        return
      }

      loadingFollowed.value = true
      try {
        const response = await api.get<Course[]>('/users/me/followed-courses')
        followedCourses.value = response.data
      } catch (error) {
        console.error('Failed to fetch followed courses:', error)
      } finally {
        loadingFollowed.value = false
      }
    }

    const fetchCourses = async () => {
      loading.value = true
      try {
        const response = await api.get<Course[]>('/courses')
        courses.value = response.data
      } catch (error) {
        console.error('Failed to fetch courses:', error)
      } finally {
        loading.value = false
      }
    }

    const searchCourses = async () => {
      if (searchQuery.value.trim() === '') {
        fetchCourses()
        return
      }
      loading.value = true
      try {
        const response = await api.get<Course[]>('/courses/search', {
          params: { q: searchQuery.value },
        })
        courses.value = response.data
      } catch (error) {
        console.error('Search failed:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchCourses()
      fetchFollowedCourses()
    })

    return {
      courses,
      followedCourses,
      loading,
      loadingFollowed,
      searchQuery,
      subjects,
      selectedSubject,
      filteredCourses,
      filteredFollowedCourses,
      selectSubject,
      searchCourses,
      truncateDescription,
      fetchFollowedCourses,
    }
  },
})
</script>

<style scoped>
.section-title {
  font-size: 1.5rem;
  color: var(--color-heading);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-border);
}

.courses-section {
  margin-bottom: 3rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  background: var(--color-background-soft);
  border-radius: 8px;
  color: var(--color-text-light-2);
}

.search-section {
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 1rem;
}

/* Subject Buttons */
.subject-filter {
  margin-top: 1rem;
}

.subject-button {
  background-color: #f4f4f4; /* Subtle background to differentiate from plain text */
  border: 1px solid #ddd;
  color: #333;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 0.5rem;
  margin-top: 0.5rem;
  transition:
    background-color 0.2s,
    color 0.2s,
    border-color 0.2s,
    box-shadow 0.2s;
}

/* Hover state */
.subject-button:hover {
  background-color: #eaeaea;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}

/* Active (selected) state */
.subject-button.is-active {
  background-color: var(--color-primary, #007BFF);
  color: #fff;
  border-color: var(--color-primary, #007BFF);
  box-shadow: none;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.course-card {
  background: var(--color-background-soft);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  height: 100%;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.course-content {
  flex: 1;
  text-decoration: none;
  color: inherit;
  padding: 1.5rem 1.5rem 0.5rem;
}

.course-header {
  margin-bottom: 1rem;
}

.course-title {
  color: var(--color-heading);
  font-size: 1.3rem;
  margin-bottom: 0.25rem;
}

.course-code {
  display: block;
  color: var(--color-text-light-2);
  font-size: 0.9rem;
  font-weight: 500;
}

.course-description {
  color: var(--color-text-light-2);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  background: var(--color-background);
  border-radius: 0 0 8px 8px;
}

.course-units {
  color: var(--color-text-light-2);
  font-size: 0.9rem;
}
</style>
