<script setup>
defineProps(['title'])
</script>

<template>
  <button class="custom-button">
    {{ title }}
  </button>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

.custom-button {
  width: 220px;
  height: 52px;
  background-color: #0a0f1c;
  border-radius: 12px;
  border: 1px solid #4e5d78;
  color: #ffffff;
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  font-weight: 500;
  text-transform: uppercase;
  transition: background-color 0.3s, border-color 0.3s, transform 0.2s;
  cursor: pointer;
}

.custom-button:hover {
  background-color: #121c2f;
  border-color: #6d88c1;
  transform: scale(1.03);
}
</style>
