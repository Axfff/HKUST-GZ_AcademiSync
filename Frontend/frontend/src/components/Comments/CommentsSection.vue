<template>
  <div class="comments-section">
    <div v-if="loading">Loading comments...</div>
    <div v-else>
      <form @submit.prevent="postComment">
        <textarea v-model="newComment" placeholder="Add a comment..." required></textarea>
        <button type="submit">Post Comment</button>
      </form>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <ul>
        <li v-for="comment in comments" :key="comment.id">
          <CommentItem :comment="comment" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import api from '../../services/api';
import CommentItem from './CommentItem.vue';

interface Comment {
  id: number;
  user_id: number;
  course_id: number | null;
  course_instructor_id: number | null;
  parent_comment_id: number | null;
  content: string;
  created_at: string;
  sub_comments?: Comment[];
}

export default defineComponent({
  name: 'CommentsSection',
  components: { CommentItem },
  props: {
    courseId: {
      type: Number,
      required: true,
    },
    instructorId: {
      type: Number,
      required: false,
    },
  },
  setup(props) {
    const comments = ref<Comment[]>([]);
    const newComment = ref('');
    const loading = ref(false);
    const errorMessage = ref('');

    const fetchComments = async () => {
      loading.value = true;
      try {
        let endpoint = '';
        if (props.instructorId) {
          endpoint = `/comments/courses/${props.courseId}/instructors/${props.instructorId}`;
        } else {
          endpoint = `/comments/courses/${props.courseId}`;
        }
        const response = await api.get<Comment[]>(endpoint);
        comments.value = response.data;
      } catch (error) {
        console.error('Failed to fetch comments:', error);
      } finally {
        loading.value = false;
      }
    };

    const postComment = async () => {
      try {
        await api.post('/comments', {
          course_id: props.courseId,
          course_instructor_id: props.instructorId || null,
          content: newComment.value,
        });
        newComment.value = '';
        fetchComments();
      } catch (error: any) {
        errorMessage.value = error.response?.data?.message || 'Failed to post comment.';
      }
    };

    onMounted(() => {
      fetchComments();
    });

    return { comments, newComment, loading, postComment, errorMessage };
  },
});
</script>

<style scoped>
.error {
  color: red;
  margin-top: 0.5rem;
}
textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 0.5rem;
}
button {
  padding: 0.5em 1em;
  background-color: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
button:hover {
  background-color: var(--color-primary-dark);
}
</style>
