<template>
  <div v-if="loading" class="preloader">Загрузка...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const loading = ref(true);

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
  }, 300); // эмуляция минимальной задержки
});
</script>

<style scoped>
.preloader {
  height: 100vh;
  background-color: black;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
