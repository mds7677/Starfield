<template>
  <Header/>
  <Preloader/>

  <div class="stars-input-wrapper">
    <MyStars />
    <MyInput />
  </div>

  <div class="page-container">
    <!-- Левая колонка с текстами -->
    <div class="floating-texts left">
      <transition-group name="fade-float" tag="div">
        <MyText
            v-for="item in floatingLeft"
            :key="item.id"
            v-bind="item"
        />
      </transition-group>
    </div>

    <!-- Правая колонка с текстами -->
    <div class="floating-texts right">
      <transition-group name="fade-float" tag="div">
        <MyText
            v-for="item in floatingRight"
            :key="item.id"
            v-bind="item"
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
import Preloader from "./components/Preloader.vue";
import Header from "./components/Header.vue";

const constellations = ref([]);
const floatingLeft = ref([]);
const floatingRight = ref([]);

function getRandomItem() {
  const index = Math.floor(Math.random() * constellations.value.length);
  return { ...constellations.value[index], id: Math.random().toString(36).substr(2, 9) };
}

function spawnFloatingBlock() {
  const leftItem = getRandomItem();
  const rightItem = getRandomItem();

  if (floatingLeft.value.length < 3) {
    floatingLeft.value.push(leftItem);
    setTimeout(() => {
      floatingLeft.value = floatingLeft.value.filter(i => i.id !== leftItem.id);
    }, 8000);
  }

  if (floatingRight.value.length < 3) {
    floatingRight.value.push(rightItem);
    setTimeout(() => {
      floatingRight.value = floatingRight.value.filter(i => i.id !== rightItem.id);
    }, 8000);
  }
}

onMounted(async () => {
  try {
    const response = await fetch('constellations_extended.json');
    const data = await response.json();
    constellations.value = data;

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
}

/* Контейнер для звёзд и инпута вертикальный, немного поднимем MyInput */
.stars-input-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding-top: 40px; /* Можно регулировать отступ сверху */
}

/* Поднимем MyInput чуть выше относительно MyStars */
.stars-input-wrapper MyInput {
  margin-top: -10px; /* Немного сдвигаем вверх */
}

/* Основной контейнер с двумя колонками */
.page-container {
  display: flex;
  justify-content: space-between; /* Колонки по краям */
  padding: 80px 40px;
  min-height: 40vh;
  gap: 20px; /* Отступ между колонками */
}

/* Колонки с текстами — убираем абсолютное позиционирование */
.floating-texts {
  position: relative; /* или можно вообще убрать */
  display: flex;
  flex-direction: column;
  gap: 20px;
  top: -650px;
  width: 300px;
  pointer-events: auto;
}

.floating-texts.left {
  /* можно добавить дополнительные стили при необходимости */
}

.floating-texts.right {
  /* можно добавить дополнительные стили при необходимости */
}

/* Анимация появления и исчезновения */
.fade-float-enter-active,
.fade-float-leave-active {
  transition: opacity 0.6s ease, transform 0.6s ease;
}

/* Появление — снизу с прозрачностью */
.fade-float-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

/* Исчезновение — уезжание в сторону + прозрачность */
.fade-float-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Для левой колонки уезжание влево */
.floating-texts.left .fade-float-leave-to {
  transform: translateX(-100%) translateY(10px);
}

/* Для правой колонки уезжание вправо */
.floating-texts.right .fade-float-leave-to {
  transform: translateX(100%) translateY(10px);
}

/* Плавное смещение элементов при изменении позиции */
.fade-float-move {
  transition: transform 0.6s ease;
}
</style>
