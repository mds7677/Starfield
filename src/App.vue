<template>
  <Header />
  <Preloader />
  <MyStars />
  <div class="main-wrapper">
    <!-- Левая колонка -->
    <div class="floating-texts left">
      <transition-group name="fade-float" tag="div">
        <MyText
            v-for="item in floatingLeft"
            :key="item.id"
            v-bind="item"
            @mouseenter="clearTimer(item.id)"
            @mouseleave="setRemovalTimer(item.id, 'left')"
        />
      </transition-group>
    </div>

    <!-- Центр -->
    <div class="stars-input-wrapper">
      <MyInput />
    </div>

    <!-- Правая колонка -->
    <div class="floating-texts right">
      <transition-group name="fade-float" tag="div">
        <MyText
            v-for="item in floatingRight"
            :key="item.id"
            v-bind="item"
            @mouseenter="clearTimer(item.id)"
            @mouseleave="setRemovalTimer(item.id, 'right')"
        />
      </transition-group>
    </div>
  </div>

  <Footer />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import MyStars from './components/Stars.vue';
import MyInput from './components/Input.vue';
import MyText from './components/Text.vue';
import Preloader from './components/Preloader.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

const constellations = ref([]);
const floatingLeft = ref([]);
const floatingRight = ref([]);
const timers = ref({});

function getRandomItem() {
  if (constellations.value.length === 0) return null;
  const index = Math.floor(Math.random() * constellations.value.length);
  return { ...constellations.value[index], id: Math.random().toString(36).substr(2, 9) };
}

function clearTimer(id) {
  if (timers.value[id]) {
    clearTimeout(timers.value[id]);
    delete timers.value[id];
  }
}

function setRemovalTimer(id, column) {
  clearTimer(id);
  const timeout = setTimeout(() => {
    if (column === 'left') {
      floatingLeft.value = floatingLeft.value.filter(i => i.id !== id);
    } else if (column === 'right') {
      floatingRight.value = floatingRight.value.filter(i => i.id !== id);
    }
    delete timers.value[id];
  }, 8000);
  timers.value[id] = timeout;
}

function spawnFloatingBlock() {
  if (constellations.value.length === 0) return;

  if (floatingLeft.value.length < 3) {
    const leftItem = getRandomItem();
    if (leftItem) {
      floatingLeft.value.push(leftItem);
      setRemovalTimer(leftItem.id, 'left');
    }
  }

  if (floatingRight.value.length < 3) {
    const rightItem = getRandomItem();
    if (rightItem) {
      floatingRight.value.push(rightItem);
      setRemovalTimer(rightItem.id, 'right');
    }
  }
}

onMounted(async () => {
  try {
    const response = await fetch('constellations_extended.json');
    const data = await response.json();
    constellations.value = data;

    spawnFloatingBlock();
    setInterval(spawnFloatingBlock, 3000);
  } catch (error) {
    console.error('Ошибка загрузки:', error);
  }
});
</script>

<style>
body {
  background-color: black;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 80px; /* увеличиваем расстояние между колонками */
  padding: 40px;
  flex-grow: 1;
}

/* Левый блок — с отступом слева */
.floating-texts.left {
  margin-right: 110px; /* отступ от левого края */
}

/* Правый блок — с отступом справа */
.floating-texts.right {
  margin-left: 80px; /* отступ от правого края */
}

.floating-texts {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 300px;
  pointer-events: auto;
  margin-top: 0 !important;
}

.floating-texts > * {
  color: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7);
  user-select: none;
  cursor: default;
  line-height: 1.4;
  min-height: 60px;
  transition: background-color 0.3s ease;
  will-change: transform;
}

.stars-input-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stars-input-wrapper MyInput {
  margin-top: 0 !important;
}

/* Анимации (оставил без изменений) */
.fade-float-enter-active,
.fade-float-leave-active {
  transition:
      opacity 1s cubic-bezier(0.4, 0, 0.2, 1),
      transform 1s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: top center;
}

.fade-float-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-float-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.floating-texts.left .fade-float-leave-to {
  transform: translateX(-40%) translateY(20px) scale(0.95);
}

.floating-texts.right .fade-float-leave-to {
  transform: translateX(40%) translateY(20px) scale(0.95);
}

.fade-float-move {
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
}

footer {
  padding: 20px 40px;
  background-color: #0a0f1c;
  color: white;
  text-align: center;
}

</style>

