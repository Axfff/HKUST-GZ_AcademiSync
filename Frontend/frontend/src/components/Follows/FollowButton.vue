<template>
  <button
    @click="toggleFollow"
    :class="['follow-button', { following: isFollowing }]"
    :disabled="loading"
  >
    <span v-if="loading">...</span>
    <template v-else>
      {{ isFollowing ? 'Following' : 'Follow' }}
    </template>
  </button>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import { useAuthStore } from '../../store/auth'

export default defineComponent({
  name: 'FollowButton',
  props: {
    courseId: {
      type: Number,
      required: true,
    },
  },
  emits: ['follow-updated'],
  setup(props, { emit }) {
    const isFollowing = ref(false)
    const loading = ref(false)
    const authStore = useAuthStore()
    const router = useRouter()

    const fetchFollowStatus = async () => {
      if (!authStore.isAuthenticated) return

      loading.value = true
      try {
        const response = await api.get('/users/me/followed-courses')
        isFollowing.value = response.data.some((course: any) => course.id === props.courseId)
      } catch (error) {
        console.error('Failed to fetch follow status:', error)
      } finally {
        loading.value = false
      }
    }

    const toggleFollow = async () => {
      if (!authStore.isAuthenticated) {
        router.push('/login')
        return
      }

      loading.value = true
      try {
        if (isFollowing.value) {
          await api.delete(`/follows/courses/${props.courseId}`)
          isFollowing.value = false
        } else {
          await api.post(`/follows/courses/${props.courseId}`)
          isFollowing.value = true
        }
        emit('follow-updated')
      } catch (error: any) {
        console.error('Failed to toggle follow:', error)
        const errorMessage = error.response?.data?.message || 'Failed to update follow status'
        console.log('Error details:', {
          status: error.response?.status,
          data: error.response?.data,
          headers: error.response?.headers,
        })
        alert(errorMessage)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      if (authStore.isAuthenticated) {
        console.log('Fetching follow status for course:', props.courseId)
        fetchFollowStatus()
      }
    })

    watch(
      () => authStore.isAuthenticated,
      (newValue) => {
        if (newValue) {
          fetchFollowStatus()
        } else {
          isFollowing.value = false
        }
      },
    )

    return { isFollowing, loading, toggleFollow }
  },
})
</script>

<style scoped>
.follow-button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  min-width: 100px;
  border: 1px solid #4a90e2;
  transition: all 0.2s ease;
}

.follow-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.follow-button:not(.following) {
  background-color: #4a90e2;
  color: white;
}

.follow-button.following {
  background-color: white;
  color: #4a90e2;
}

.follow-button:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
