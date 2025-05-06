<script setup>
defineProps(["title","head"]);
</script>

<template>
<div>
  <h2>{{ head }}</h2>
  {{ title }}<hr>
</div>
</template>

<style scoped>
hr{
  width: 260px;
}
div{
  opacity: 0;
  transform: translateY(30px);
  animation: fadeUp 1.3s ease-out forwards;
  font-size: 17px;
  position: relative;
  width: 300px;
  font-family:InterFace;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>