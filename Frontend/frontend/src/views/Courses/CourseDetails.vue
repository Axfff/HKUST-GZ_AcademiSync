<template>
  <div v-if="loading" class="loading">Loading course details...</div>
  <div v-else-if="course" class="course-details-container">
    <div class="course-header">
      <h1 class="course-title">{{ course.name }}</h1>
      <span class="course-code">{{ course.course_code }}</span>
    </div>
    <p class="course-description">{{ course.description }}</p>

    <div class="section">
      <h2 class="section-title">Instructors</h2>
      <div v-if="course.instructors?.length" class="instructors-grid">
        <div
          v-for="instructor in course.instructors"
          :key="instructor.id"
          :class="['instructor-card', { active: selectedInstructor?.id === instructor.id }]"
          @click="toggleInstructor(instructor)"
        >
          <h3>{{ instructor.name }}</h3>
          <p>{{ instructor.department }}</p>
        </div>
      </div>
      <p v-else>No instructors assigned to this course.</p>
    </div>

    <div class="section">
      <div class="section-header">
        <h2 class="section-title">Ratings</h2>
        <span v-if="selectedInstructor" class="selected-context">
          for {{ selectedInstructor.name }}
          <button class="clear-selection" @click="clearInstructorSelection">×</button>
        </span>
      </div>
      <RatingsSection :course-id="Number(courseId)" :instructor-id="selectedInstructor?.id" />
    </div>

    <div class="section">
      <div class="section-header">
        <h2 class="section-title">Comments</h2>
        <span v-if="selectedInstructor" class="selected-context">
          for {{ selectedInstructor.name }}
          <button class="clear-selection" @click="clearInstructorSelection">×</button>
        </span>
      </div>
      <CommentsSection :course-id="Number(courseId)" :instructor-id="selectedInstructor?.id" />
    </div>

    <div class="section">
      <FollowButton :course-id="Number(courseId)" />
    </div>
  </div>
  <div v-else class="error">Course not found</div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../services/api'
import FollowButton from '../../components/Follows/FollowButton.vue'
import RatingsSection from '../../components/Ratings/RatingsSection.vue'
import CommentsSection from '../../components/Comments/CommentsSection.vue'

interface Instructor {
  course_instructor_id: number
  id: number
  name: string
  department: string
  profile_url: string
  created_at: string
}

interface CourseDetails {
  id: number
  course_code: string
  name: string
  description: string
  created_at: string
  instructors: Instructor[]
}

export default defineComponent({
  name: 'CourseDetails',
  components: {
    FollowButton,
    RatingsSection,
    CommentsSection,
  },
  setup() {
    const route = useRoute()
    const courseId = route.params.id as string
    const course = ref<CourseDetails | null>(null)
    const loading = ref(true)
    const selectedInstructor = ref<Instructor | null>(null)

    const toggleInstructor = (instructor: Instructor) => {
      if (selectedInstructor.value?.id === instructor.id) {
        selectedInstructor.value = null
      } else {
        selectedInstructor.value = instructor
      }
    }

    const clearInstructorSelection = () => {
      selectedInstructor.value = null
    }

    const fetchCourseDetails = async () => {
      loading.value = true
      try {
        const response = await api.get<CourseDetails>(`/courses/${courseId}`)
        course.value = response.data
      } catch (error) {
        console.error('Failed to fetch course details:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchCourseDetails()
    })

    return {
      course,
      loading,
      courseId,
      selectedInstructor,
      toggleInstructor,
      clearInstructorSelection,
    }
  },
})
</script>

<style scoped>
.course-details-container {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.course-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 1rem 0;
}

.course-units {
  font-weight: 500;
  color: var(--color-text-light-2);
  margin: 0.5rem 0;
}

.section {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--color-heading);
}

.instructors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.instructor-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.instructor-card.active {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.instructor-card h3 {
  margin-bottom: 0.5rem;
  color: var(--color-heading);
}

.course-header {
  margin-bottom: 1.5rem;
}

.course-title {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.course-code {
  display: block;
  color: var(--color-text-light-2);
  font-size: 1.1rem;
  font-weight: 500;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.selected-context {
  font-size: 0.9rem;
  color: var(--color-text-light-2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.clear-selection {
  background: none;
  border: none;
  color: var(--color-text-light-2);
  cursor: pointer;
  padding: 0 0.5rem;
  font-size: 1.2rem;
  line-height: 1;
}

.clear-selection:hover {
  color: var(--color-text);
}
</style>
