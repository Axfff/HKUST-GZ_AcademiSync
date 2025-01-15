<template>
  <div class="ratings-section">
    <div v-if="loadingAggregates" class="loading">Loading ratings...</div>
    <div v-else-if="aggregatedRatings.length" class="ratings-grid">
      <div
        v-for="rating in aggregatedRatings"
        :key="rating.dimension_id"
        class="rating-item"
      >
        <div class="rating-header">
          <h3 class="dimension-name">{{ rating.dimension_name }}</h3>
          <div class="average-rating">
            Average:
            {{
              rating.average_score !== null
                ? (typeof rating.average_score === 'string'
                  ? parseFloat(rating.average_score).toFixed(1)
                  : rating.average_score.toFixed(1))
                : "No ratings yet"
            }}
          </div>
        </div>
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
  average_score: string | number | null;
  score?: number | null;
}

interface MyRatingData {
  dimension_id: number;
  dimension_name: string;
  score: number | null;
}

interface AggregatedRating extends RatingData {
  average_score: string | number | null;
}

export default defineComponent({
  name: "RatingsSection",
  components: { StarRating },
  props: {
    courseId: { type: Number, required: true },
    instructorId: { type: Number, required: false },
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
          ? `/ratings/my-ratings?course_instructor_id=${courseInstructorId.value.toString()}`
          : `/ratings/my-ratings?course_id=${props.courseId}`;
        console.log("Fetching user ratings with endpoint:", endpoint);
        const response = await api.get<{ ratings: MyRatingData[] }>(endpoint);
        console.log("Received user ratings:", response.data);
        const ratings = response.data.ratings || [];
        userRatings.value = ratings.reduce(
          (acc: Record<number, number>, rating: MyRatingData) => {
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
  padding: 1rem;
}

.ratings-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.rating-item {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  min-width: 0;
}

.rating-header {
  margin-bottom: 0.75rem;
}

.dimension-name {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.average-rating {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.rating-input-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.star-rating-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rating-score {
  font-size: 0.9rem;
  color: #666;
}

.submit-rating-btn {
  padding: 0.4rem 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  width: 100%;
}

.submit-rating-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-rating-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.success-message {
  color: #4CAF50;
  margin-top: 1rem;
}

.error-message {
  color: #f44336;
  margin-top: 1rem;
}

.loading {
  color: #666;
  font-style: italic;
}

@media (max-width: 1200px) {
  .ratings-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .ratings-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .ratings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
