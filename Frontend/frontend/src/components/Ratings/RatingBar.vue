<template>
  <div class="rating-bar-container">
    <StarRating
      :model-value="userScore || 0"
      show-stars
      @update:modelValue="handleRating"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import StarRating from './StarRating.vue';
import api from '../../services/api';

export default defineComponent({
  name: 'RatingBar',
  components: { StarRating },
  props: {
    averageScore: { type: Number, required: true },
    userScore: { type: Number, default: 0 },
    dimensionId: { type: Number, required: true },
  },
  emits: ['submit-rating'],
  setup(props, { emit }) {
    const handleRating = (score: number) => {
      emit('submit-rating', {
        dimensionId: props.dimensionId,
        score,
      });
    };

    return { handleRating };
  },
});
</script>

<style scoped>
.rating-bar-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
