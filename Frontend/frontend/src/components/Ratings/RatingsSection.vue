<template>
  <div class="ratings-section">
    <div v-if="loadingAggregates" class="loading">Loading ratings...</div>
    <div v-else-if="aggregatedRatings.length" class="ratings-grid">
      <div
        v-for="rating in aggregatedRatings"
        :key="rating.dimension_id"
        class="rating-card"
      >
        <span class="dimension-name">{{ rating.dimension_name }}</span>
        <RatingBar
          :score="rating.weighted_score || 0"
          :dimension-id="rating.dimension_id"
          :user-score="userRatings[rating.dimension_id]"
          @submit-rating="handleRatingSubmit"
        />
      </div>
    </div>
    <p v-if="message" :class="{ 'success-message': success, 'error-message': !success }">
      {{ message }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import api from '../../services/api'
import RatingBar from './RatingBar.vue'

interface RatingData {
  dimension_id: number
  dimension_name: string
  average_score: number | null
  user_score?: number
}

interface AggregatedRating extends RatingData {
  weighted_score: number | null
}

export default defineComponent({
  name: 'RatingsSection',
  components: { RatingBar },
  props: {
    courseId: { type: Number, required: true },
    instructorId: { type: Number, default: null },
  },
  setup(props) {
    const aggregatedRatings = ref<AggregatedRating[]>([])
    const userRatings = ref<Record<number, number>>({})
    const loadingAggregates = ref(false)
    const message = ref('')
    const success = ref(true)

    const fetchUserRatings = async () => {
      try {
        const endpoint = props.instructorId
          ? `/ratings/my-ratings?course_instructor_id=${props.instructorId}`
          : `/ratings/my-ratings?course_id=${props.courseId}`
        const response = await api.get(endpoint)
        const ratings = response.data.ratings || []
        userRatings.value = ratings.reduce((acc: Record<number, number>, rating: RatingData) => {
          acc[rating.dimension_id] = rating.score || 0
          return acc
        }, {})
      } catch (error) {
        console.error('Failed to fetch user ratings:', error)
      }
    }

    const handleRatingSubmit = async (rating: { dimensionId: number; score: number }) => {
      try {
        const payload = props.instructorId
          ? {
              course_instructor_id: props.instructorId,
              ratings: [{
                rating_dimension_id: rating.dimensionId,
                score: rating.score,
              }],
            }
          : {
              course_id: props.courseId,
              ratings: [{
                rating_dimension_id: rating.dimensionId,
                score: rating.score,
              }],
            }

        await api.post('/ratings', payload)
        message.value = 'Rating submitted successfully'
        success.value = true
        userRatings.value[rating.dimensionId] = rating.score
        fetchAggregatedRatings()
      } catch (error: any) {
        message.value = error.response?.data?.message || 'Failed to submit rating'
        success.value = false
      }
    }

    const calculateWeightedScores = async () => {
      if (props.instructorId) {
        const response = await api.get<{ ratings: RatingData[] }>(
          `/ratings/courses/${props.courseId}/instructors/${props.instructorId}`
        )
        return response.data.ratings.map((rating) => ({
          ...rating,
          weighted_score: rating.average_score,
        }))
      } else {
        const response = await api.get<{ ratings: RatingData[] }>(
          `/ratings/courses/${props.courseId}`
        )
        return response.data.ratings.map((rating) => ({
          ...rating,
          weighted_score: rating.average_score,
        }))
      }
    }

    const fetchAggregatedRatings = async () => {
      loadingAggregates.value = true
      message.value = ''
      try {
        aggregatedRatings.value = await calculateWeightedScores()

        // Initialize scores with default values
        aggregatedRatings.value.forEach((rating) => {
          scores[rating.dimension_id] = 5
        })
      } catch (error) {
        console.error('Failed to fetch ratings:', error)
        message.value = 'Failed to load ratings. Please try again later.'
        success.value = false
        aggregatedRatings.value = []
      } finally {
        loadingAggregates.value = false
      }
    }

    watch(() => props.instructorId, () => {
      fetchAggregatedRatings()
      fetchUserRatings()
    })

    onMounted(() => {
      fetchAggregatedRatings()
      fetchUserRatings()
    })

    return {
      aggregatedRatings,
      userRatings,
      loadingAggregates,
      handleRatingSubmit,
      message,
      success,
    }
  },
})
</script>

<style scoped>
.ratings-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ratings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.rating-card {
  background: var(--color-background);
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid var(--color-border);
}

.dimension-name {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-heading);
}

.success-message {
  color: #28a745;
  text-align: center;
}

.error-message {
  color: #dc3545;
  text-align: center;
}

.progress-bar {
  position: relative;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4caf50;
  transition: width 0.3s ease;
}

.average-score {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.9rem;
  color: #fff;
}
</style>
