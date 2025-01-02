<template>
  <div class="dashboard">
    <h2>Your Followed Courses</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <ul>
        <li v-for="course in followedCourses" :key="course.id">
          <router-link :to="`/courses/${course.id}`">
            {{ course.course_code }} - {{ course.title }}
          </router-link>
        </li>
      </ul>
      <div v-if="!followedCourses.length">You are not following any courses.</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import api from '../services/api';

interface Course {
  id: number;
  course_code: string;
  title: string;
  unit: number;
  description: string;
  created_at: string;
}

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const followedCourses = ref<Course[]>([]);
    const loading = ref(false);

    const fetchFollowedCourses = async () => {
      loading.value = true;
      try {
        const response = await api.get<Course[]>('/users/me/followed-courses');
        followedCourses.value = response.data;
      } catch (error) {
        console.error('Failed to fetch followed courses:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchFollowedCourses();
    });

    return { followedCourses, loading };
  },
});
</script>

<style scoped>
/* Add your styles here */
</style>
