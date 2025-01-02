<template>
  <div class="star-rating" v-if="showStars">
    <button
      v-for="star in 5"
      :key="star"
      class="star-button"
      :class="{ active: star <= modelValue }"
      @click="$emit('update:modelValue', star)"
      type="button"
    >
      ★
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'StarRating',
  props: {
    modelValue: {
      type: Number,
      required: true,
    },
    showStars: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue'],
})
</script>

<style scoped>
.star-rating {
  display: flex;
  gap: 0.25rem;
}

.star-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0;
  color: var(--color-text-light-2);
  transition: color 0.2s ease;
}

.star-button.active {
  color: #ffc107;
}

.star-button:hover {
  color: #ffc107;
}
</style>
