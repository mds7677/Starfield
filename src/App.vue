<template>
  <Header/>
  <Preloader/>

  <div style="display: flex; flex-direction: column;width: 100vw">
    <MyStars />
    <MyInput />
  </div>

  <div class="conveyor-fade-wrapper">
    <div class="fade-left"></div>
    <div class="fade-right"></div>

<!--    <div class="conveyor" @mouseover="pause" @mouseleave="resume">
      <div
          class="conveyor-item"
          v-for="post in constellations"
          :key="post.id"
      >
        <MyText
            :title="post.title"
            :head="post.head"
            :body="post.body"
            :image="post.image"
        />
      </div>
    </div>-->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import MyStars from './components/Stars.vue';
import MyInput from './components/Input.vue';
import MyText from './components/Text.vue';
import MyButton from './components/MenuButton.vue';
import Preloader from "./components/Preloader.vue";
import Header from "./components/Header.vue";

const constellations = ref([]);
const isPaused = ref(false);

onMounted(async () => {
  try {
    const response = await fetch('constellations_extended.json');
    const data = await response.json();
    // Дублируем для бесконечной прокрутки
    constellations.value = [...data, ...data];
  } catch (error) {
    console.error('Ошибка загрузки:', error);
  }
});

const pause = () => {
  isPaused.value = true;
  const conveyor = document.querySelector('.conveyor');
  conveyor.style.animationPlayState = 'paused';
};

const resume = () => {
  isPaused.value = false;
  const conveyor = document.querySelector('.conveyor');
  conveyor.style.animationPlayState = 'running';
};
</script>

<style>
body {
  background-color: black;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}
/* Пример: временная заглушка */
.my-stars-placeholder,
.my-input-placeholder {
  min-height: 100px; /* или что подходит по макету */
}

/* Обёртка с градиентами */
.conveyor-fade-wrapper {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
  padding: 20px 0;
  margin-top:10px;
}

.conveyor {
  display: flex;
  gap: 20px;
  animation: scroll-left 200s linear infinite;
  width: max-content;
  padding: 0 40px;
  margin-bottom: 250px;
}

.conveyor-item {
  flex-shrink: 0;
  width: 300px;
}

/* Градиентные края */
.fade-left,
.fade-right {
  position: absolute;
  top: 0;
  width: 60px;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

.fade-left {
  left: 0;
  background: linear-gradient(to right, black 0%, transparent 100%);
}

.fade-right {
  right: 0;
  background: linear-gradient(to left, black 0%, transparent 100%);
}

/* Анимация движения */
@keyframes scroll-left {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>