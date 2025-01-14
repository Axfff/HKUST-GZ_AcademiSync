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
        <div class="rating-input-container">
          <div class="star-rating-container">
            <StarRating
              :model-value="
                pendingRatings[rating.dimension_id] ||
                userRatings[rating.dimension_id] ||
                0
              "
              show-stars
              @update:model-value="
                (score) =>
                  handleRatingSubmit({
                    dimensionId: rating.dimension_id,
                    score,
                  })
              "
            />
            <span class="rating-score"
              >{{
                pendingRatings[rating.dimension_id] ||
                userRatings[rating.dimension_id] ||
                0
              }}/5</span
            >
          </div>
          <button
            class="submit-rating-btn"
            @click="submitDimensionRating(rating.dimension_id)"
            :disabled="!pendingRatings[rating.dimension_id]"
          >
            Submit Rating
          </button>
        </div>
        <div class="average-rating">
          Average:
          {{
            rating.average_score
              ? parseFloat(rating.average_score).toFixed(1)
              : "No ratings yet"
          }}
        </div>
      </div>
    </div>
    <p
      v-if="message"
      :class="{ 'success-message': success, 'error-message': !success }"
    >
      {{ message }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch, reactive } from "vue";
import api from "../../services/api";
import StarRating from "./StarRating.vue";

interface RatingData {
  dimension_id: number;
  dimension_name: string;
  average_score: number | null;
  user_score?: number;
}

interface AggregatedRating extends RatingData {
  average_score: number | null;
}

export default defineComponent({
  name: "RatingsSection",
  components: { StarRating },
  props: {
    courseId: { type: Number, required: true },
    instructorId: { type: Number, default: null },
  },
  setup(props) {
    const aggregatedRatings = ref<AggregatedRating[]>([]);
    const userRatings = ref<Record<number, number>>({});
    const pendingRatings = reactive<Record<number, number>>({});
    const loadingAggregates = ref(false);
    const message = ref("");
    const success = ref(true);
    const courseInstructorId = ref<number | null>(null);

    const fetchUserRatings = async () => {
      try {
        const endpoint = courseInstructorId.value
          ? `/ratings/my-ratings?course_instructor_id=${courseInstructorId.value}`
          : `/ratings/my-ratings?course_id=${props.courseId}`;
        console.log("Fetching user ratings with endpoint:", endpoint);
        const response = await api.get(endpoint);
        console.log("Received user ratings:", response.data);
        const ratings = response.data.ratings || [];
        userRatings.value = ratings.reduce(
          (acc: Record<number, number>, rating: RatingData) => {
            acc[rating.dimension_id] = rating.score || 0;
            return acc;
          },
          {}
        );
        console.log("Processed user ratings:", userRatings.value);
      } catch (error) {
        console.error("Failed to fetch user ratings:", error);
      }
    };

    const handleRatingSubmit = (rating: {
      dimensionId: number;
      score: number;
    }) => {
      pendingRatings[rating.dimensionId] = rating.score;
    };

    const submitDimensionRating = async (dimensionId: number) => {
      try {
        const score = pendingRatings[dimensionId];
        console.log("Submitting rating with payload:", {
          dimensionId,
          score,
          courseId: props.courseId,
          courseInstructorId: courseInstructorId.value,
        });
        const payload = courseInstructorId.value
          ? {
              course_instructor_id: courseInstructorId.value,
              ratings: [
                {
                  rating_dimension_id: dimensionId,
                  score: score,
                },
              ],
            }
          : {
              course_id: props.courseId,
              ratings: [
                {
                  rating_dimension_id: dimensionId,
                  score: score,
                },
              ],
            };

        console.log("Making API request with payload:", payload);
        const response = await api.post("/ratings", payload);
        console.log("Rating submission response:", response);
        message.value = "Rating submitted successfully";
        success.value = true;
        userRatings.value[dimensionId] = score;
        delete pendingRatings[dimensionId];
        await fetchAggregatedRatings();
        console.log("Updated aggregated ratings:", aggregatedRatings.value);
      } catch (error: any) {
        console.error("Failed to submit rating:", error);
        message.value =
          error.response?.data?.message || "Failed to submit rating";
        success.value = false;
      }
    };

    const calculateWeightedScores = async () => {
      try {
        if (props.instructorId) {
          const response = await api.get<{ ratings: RatingData[]; course_instructor_id: number }>(
            `/ratings/courses/${props.courseId}/instructors/${props.instructorId}`
          );
          console.log("Received instructor ratings:", response.data);
          courseInstructorId.value = response.data.course_instructor_id;
          return response.data.ratings.map((rating) => ({
            ...rating,
            dimension_id: rating.dimension_id,
            dimension_name: rating.dimension_name,
            average_score:
              rating.average_score !== null
                ? typeof rating.average_score === "string"
                  ? parseFloat(rating.average_score)
                  : rating.average_score
                : null,
          }));
        } else {
          const response = await api.get<{ ratings: RatingData[] }>(
            `/ratings/courses/${props.courseId}`
          );
          console.log("Received course ratings:", response.data);
          courseInstructorId.value = null;
          return response.data.ratings.map((rating) => ({
            ...rating,
            dimension_id: rating.dimension_id,
            dimension_name: rating.dimension_name,
            average_score:
              rating.average_score !== null
                ? typeof rating.average_score === "string"
                  ? parseFloat(rating.average_score)
                  : rating.average_score
                : null,
          }));
        }
      } catch (error) {
        console.error("Failed to calculate weighted scores:", error);
        return [];
      }
    };

    const fetchAggregatedRatings = async () => {
      loadingAggregates.value = true;
      message.value = "";
      try {
        console.log("Fetching aggregated ratings...");
        const ratings = await calculateWeightedScores();
        console.log("Received ratings:", ratings);
        aggregatedRatings.value = ratings;
        if (ratings.length === 0) {
          message.value = "No rating dimensions available.";
          success.value = false;
        }
      } catch (error) {
        console.error("Failed to fetch ratings:", error);
        message.value = "Failed to load ratings. Please try again later.";
        success.value = false;
        aggregatedRatings.value = [];
      } finally {
        loadingAggregates.value = false;
      }
    };

    watch(
      () => props.instructorId,
      () => {
        fetchAggregatedRatings();
        fetchUserRatings();
      }
    );

    onMounted(() => {
      fetchAggregatedRatings();
      fetchUserRatings();
    });

    return {
      aggregatedRatings,
      userRatings,
      pendingRatings,
      loadingAggregates,
      handleRatingSubmit,
      submitDimensionRating,
      message,
      success,
    };
  },
});
</script>

<style scoped>
.ratings-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
}

.ratings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.rating-card {
  background: var(--color-background-soft, #ffffff);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--color-border, #e5e7eb);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.rating-input-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.star-rating-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-score {
  font-size: 1rem;
  color: var(--color-text, #374151);
}

.submit-rating-btn {
  padding: 0.75rem 1rem;
  background-color: var(--color-primary, #3b82f6);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
  width: 100%;
}

.submit-rating-btn:hover:not(:disabled) {
  background-color: var(--color-primary-dark, #2563eb);
}

.submit-rating-btn:disabled {
  background-color: var(--color-text-light-2, #9ca3af);
  cursor: not-allowed;
}

.dimension-name {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--color-heading, #111827);
}

.average-rating {
  margin-top: 1rem;
  color: var(--color-text-light-1, #6b7280);
  font-size: 0.9rem;
}

.success-message {
  color: #059669;
  text-align: center;
  padding: 0.75rem;
  background-color: #d1fae5;
  border-radius: 6px;
}

.error-message {
  color: #dc2626;
  text-align: center;
  padding: 0.75rem;
  background-color: #fee2e2;
  border-radius: 6px;
}

.loading {
  text-align: center;
  color: var(--color-text-light-1, #6b7280);
  padding: 2rem;
}
</style>
