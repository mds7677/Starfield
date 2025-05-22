<script setup>

</script>

<template>
  <p>STARFIELD</p>
</template>

<style scoped>
p {
  font-family: 'Orbitron', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0;
  padding: 16px 24px;
  border-radius: 16px;
  background: radial-gradient(ellipse at center, #0a0f1c, rgba(0, 0, 0, 0.8));
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  text-shadow: 0 0 8px rgba(0, 150, 255, 0.4);
  animation: fadeUp 1.3s ease-out forwards;
}

@keyframes fadeInTitle {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>