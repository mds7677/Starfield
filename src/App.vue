<template>
  <Header />
  <Preloader />

  <div class="stars-input-wrapper">
    <MyStars />
    <MyInput />
  </div>

  <div class="page-container">
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
</template>

<script setup>
import { ref, onMounted } from 'vue';
import MyStars from './components/Stars.vue';
import MyInput from './components/Input.vue';
import MyText from './components/Text.vue';
import Preloader from './components/Preloader.vue';
import Header from './components/Header.vue';

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
}

.stars-input-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding-top: 40px;
}

.stars-input-wrapper MyInput {
  margin-top: -10px;
}

.page-container {
  display: flex;
  justify-content: space-between;
  padding: 80px 40px;
  min-height: 40vh;
  gap: 20px;
}

.floating-texts {
  /* Убираем position: relative, чтобы элементы были в потоке */
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 300px;
  pointer-events: auto;
}

/* Стили для текстовых блоков */
.floating-texts > * {
  color: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7);
  user-select: none;
  cursor: default;
  line-height: 1.4;
  margin-top: -670px;
  transition: background-color 0.3s ease;
  /* фиксируем высоту, чтобы избежать прыжков */
  min-height: 60px;
  /* Оптимизация для анимации transform */
  will-change: transform;
}

.floating-texts > *:hover {
}

/* Анимации для переходов */
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

/* Плавное смещение элементов при перестановке */
.fade-float-move {
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

