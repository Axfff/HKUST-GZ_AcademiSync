<template>
  <div class="star-rating">
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
  },
  emits: ['update:modelValue'],
})
</script>

<style scoped>
.star-rating {
  display: inline-flex;
  gap: 0.25rem;
}

.star-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0.25rem;
  color: var(--color-text-light-2, #9ca3af);
  transition: all 0.2s ease;
}

.star-button.active {
  color: #ffc107;
  transform: scale(1.1);
}

.star-button:hover {
  color: #ffc107;
  transform: scale(1.1);
}

.star-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
  border-radius: 4px;
}
</style>
