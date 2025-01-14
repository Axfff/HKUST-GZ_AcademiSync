<template>
  <div class="dashboard-container">
    <!-- Subject Filter Sidebar -->
    <div class="sidebar">
      <h3>Subjects</h3>
      <div class="filter-group">
        <div 
          v-for="subject in subjects" 
          :key="subject"
          class="filter-item"
          :class="{ active: selectedSubject === subject }"
          @click="selectSubject(subject)"
        >
          {{ subject }}
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <h2>Your Followed Courses</h2>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <ul class="course-list">
          <li v-for="course in filteredCourses" :key="course.id" class="course-item">
            <router-link :to="`/courses/${course.id}`">
              {{ course.course_code }} - {{ course.title }}
            </router-link>
          </li>
        </ul>
        <div v-if="!filteredCourses.length">No courses found.</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
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
    const selectedSubject = ref('');

    const subjects = [
      'UCMP', 'UCUG', 'UFUG', 'UGOD', 'AIAA', 'AMAT', 'BSBE', 
      'CMAA', 'DSAA', 'EOAS', 'FTEC', 'FUNH', 'INFH', 'INTR', 
      'IOTA', 'IPEN', 'LANG', 'MICS', 'PDEV', 'PLED', 'ROAS', 
      'SEEN', 'SMMG', 'SOCH', 'SYSH'
    ];

    const filteredCourses = computed(() => {
      if (!selectedSubject.value) return followedCourses.value;
      return followedCourses.value.filter(course => 
        course.course_code.startsWith(selectedSubject.value + ' ')
      );
    });

    const selectSubject = (subject: string) => {
      selectedSubject.value = selectedSubject.value === subject ? '' : subject;
    };

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

    return {
      followedCourses,
      loading,
      subjects,
      selectedSubject,
      filteredCourses,
      selectSubject,
      fetchFollowedCourses
    };
  }
});
</script>

<style scoped>
.dashboard-container {
  display: flex;
  gap: 2rem;
  padding: 1rem;
}

.sidebar {
  width: 200px;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  height: fit-content;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-item {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.filter-item:hover {
  background-color: #e0e0e0;
}

.filter-item.active {
  background-color: #4CAF50;
  color: white;
}

.main-content {
  flex: 1;
}

.course-list {
  list-style: none;
  padding: 0;
}

.course-item {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

.course-item a {
  text-decoration: none;
  color: #333;
}

.course-item a:hover {
  color: #4CAF50;
}
</style>
