<template>
  <div class="comments-section">
    <div v-if="loading" class="loading">Loading comments...</div>
    <div v-else>
      <form @submit.prevent="postComment" class="comment-form">
        <div class="form-header">Add your comment</div>
        <textarea 
          v-model="newComment" 
          placeholder="Share your thoughts about this course..." 
          :disabled="posting"
          required
          maxlength="500"
          class="comment-textarea"
        ></textarea>
        <div class="comment-form-footer">
          <span class="char-count" :class="{ 'char-count-limit': newComment.length >= 450 }">
            {{ newComment.length }}/500 characters
          </span>
          <button 
            type="submit" 
            :disabled="posting || newComment.trim().length === 0"
            class="submit-comment-btn"
          >
            <span class="submit-icon">✉</span>
            {{ posting ? 'Posting...' : 'Post Comment' }}
          </button>
        </div>
      </form>
      
      <div v-if="errorMessage" class="message error">
        <span class="message-icon">⚠</span>
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="message success">
        <span class="message-icon">✓</span>
        {{ successMessage }}
      </div>
      
      <div class="comments-container">
        <div v-if="!loading && comments.length === 0" class="empty-state">
          <div class="empty-icon">💭</div>
          <p>No comments yet. Be the first to share your thoughts!</p>
        </div>
        
        <ul v-if="comments.length > 0" class="comments-list">
          <li v-for="comment in comments" :key="comment.id" class="comment-item-container">
            <CommentItem :comment="comment" />
          </li>
        </ul>
      </div>
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
    const posting = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

    const fetchComments = async () => {
      loading.value = true;
      errorMessage.value = '';
      try {
        let endpoint = '';
        if (props.instructorId) {
          endpoint = `/comments/courses/${props.courseId}/instructors/${props.instructorId}`;
        } else {
          endpoint = `/comments/courses/${props.courseId}`;
        }
        const response = await api.get<Comment[]>(endpoint);
        comments.value = response.data.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
      } catch (error: any) {
        errorMessage.value = error.response?.data?.message || 'Failed to load comments. Please try again later.';
      } finally {
        loading.value = false;
      }
    };

    const postComment = async () => {
      if (newComment.value.trim().length === 0) return;
      
      posting.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        await api.post('/comments', {
          course_id: props.courseId,
          course_instructor_id: props.instructorId || null,
          content: newComment.value.trim(),
        });
        
        newComment.value = '';
        successMessage.value = 'Comment posted successfully!';
        fetchComments();
      } catch (error: any) {
        errorMessage.value = error.response?.data?.message || 'Failed to post comment.';
      } finally {
        posting.value = false;
      }
    };

    onMounted(() => {
      fetchComments();
    });

    return { 
      comments, 
      newComment, 
      loading, 
      posting,
      postComment, 
      errorMessage,
      successMessage 
    };
  },
});
</script>

<style scoped>
.comments-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1rem;
}

.form-header {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading, #111827);
  margin-bottom: 0.5rem;
}

.comment-form {
  background: var(--color-background-soft, #ffffff);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--color-border, #e5e7eb);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.comment-textarea {
  width: 100%;
  min-height: 120px;
  padding: 0.75rem;
  border: 1px solid var(--color-border, #e5e7eb);
  border-radius: 6px;
  resize: vertical;
  font-size: 1rem;
  line-height: 1.5;
  transition: border-color 0.2s ease;
}

.comment-textarea:focus {
  outline: none;
  border-color: var(--color-primary, #3b82f6);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.comment-form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.char-count {
  color: var(--color-text-light-2, #9ca3af);
  font-size: 0.875rem;
}

.char-count-limit {
  color: #f59e0b;
}

.submit-comment-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary, #3b82f6);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-comment-btn:hover:not(:disabled) {
  background-color: var(--color-primary-dark, #2563eb);
}

.submit-comment-btn:disabled {
  background-color: var(--color-text-light-2, #9ca3af);
  cursor: not-allowed;
}

.submit-icon {
  font-size: 1.1rem;
}

.message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 6px;
  font-weight: 500;
}

.message-icon {
  font-size: 1.2rem;
}

.error {
  background-color: #fee2e2;
  color: #dc2626;
}

.success {
  background-color: #d1fae5;
  color: #059669;
}

.comments-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--color-text-light-1, #6b7280);
  background: var(--color-background-soft, #ffffff);
  border-radius: 8px;
  border: 1px solid var(--color-border, #e5e7eb);
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.comments-list {
  list-style-type: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item-container {
  background: var(--color-background-soft, #ffffff);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border, #e5e7eb);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  color: var(--color-text-light-1, #6b7280);
  padding: 2rem;
}
</style>
