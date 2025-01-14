<template>
  <div class="comment-item">
    <p><strong>User {{ comment.user_id }}</strong> - {{ formatDate(comment.created_at) }}</p>
    <p>{{ comment.content }}</p>
    <button @click="toggleLike">{{ liked ? 'Unlike' : 'Like' }}</button>
    <span>{{ likeCount }}</span>
    <!-- Add functionality for sub-comments if needed -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import type { PropType } from 'vue';
import api from '../../services/api';

interface Comment {
  id: number;
  user_id: number;
  course_id: number | null;
  course_instructor_id: number | null;
  parent_comment_id: number | null;
  content: string;
  created_at: string;
}

export default defineComponent({
  name: 'CommentItem',
  props: {
    comment: {
      type: Object as PropType<Comment>,
      required: true,
    },
  },
  setup(props) {
    const liked = ref(false);
    const likeCount = ref(0);

    const fetchLikeStatus = async () => {
      // Implement an API endpoint to check if the current user liked the comment
      // For demonstration, we'll assume the user hasn't liked it
      liked.value = false;
      likeCount.value = 0; // Ideally, fetch the actual like count
    };

    const toggleLike = async () => {
      try {
        if (liked.value) {
          const response = await api.delete(`/likes/comments/${props.comment.id}`);
          likeCount.value = response.data.like_count;
          liked.value = false;
        } else {
          const response = await api.post(`/likes/comments/${props.comment.id}`);
          likeCount.value = response.data.like_count;
          liked.value = true;
        }
      } catch (error) {
        console.error('Failed to toggle like:', error);
      }
    };

    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr);
      return date.toLocaleString();
    };

    onMounted(() => {
      fetchLikeStatus();
    });

    return { liked, likeCount, toggleLike, formatDate };
  },
});
</script>

<style scoped>
.comment-item {
  border-bottom: 1px solid #ccc;
  padding: 1em 0;
}
button {
  margin-right: 0.5em;
}
</style>
