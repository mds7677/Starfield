<template>
  <div
      class="wrapper"
      :class="{ mounted: isMounted }"
      @mouseover="Visible = true"
      @mouseleave="Visible = false"
  >
    <h2>{{ head }}</h2>
    <div class="title">
      {{ title }}
      <font-awesome-icon icon="chevron-down" v-if="!Visible" />
    </div>

    <div :class="['body-text', { visible: Visible }]">
      <img :src="`/illustrations/${image}`" :alt="head" />
      <p class="paragraph">{{ body }}</p>
    </div>

    <hr :class="{ shifted: Visible }" class="line" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  props: ['title', 'body', 'head', 'image'],
  setup() {
    const Visible = ref(false);
    const isMounted = ref(false);

    onMounted(() => {
      setTimeout(() => {
        isMounted.value = true;
      }, 100);
    });

    return { Visible, isMounted };
  }
};
</script>

<style scoped>
.wrapper {
  width: 300px;
  font-family: InterFace;
  opacity: 0;
  text-align: left;
  margin: 0;
  color: white;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
  overflow: hidden; /* чтобы не скакало */
}

.wrapper.mounted {
  opacity: 1;
  transform: translateY(0);
}

.title {
  font-size: 17px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* body-text скрыта по умолчанию, но с плавным max-height */
.body-text {
  max-height: 0;
  opacity: 0;
  transition: max-height 0.6s ease, opacity 0.4s ease;
  margin-top: 10px;
  font-size: 17px;
  padding-left: 22px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.body-text.visible {
  max-height: 400px; /* или чуть больше, чтобы весь текст влазил */
  opacity: 1;
}

/* линия */
.line {
  width: 260px;
  border: none;
  height: 1px;
  background: white;
  margin-top: 10px;
  transform: translateY(0);
  opacity: 0;
  transition: transform 0.8s cubic-bezier(0.25, 1.5, 0.5, 1), opacity 0.6s ease;
}

.line.shifted {
  transform: translateY(40px);
  opacity: 1;
}

/* изображение */
img {
  width: 120px;
  height: 120px;
  object-fit: contain;
  align-self: center;
  margin-bottom: 10px;
}

/* текст под изображением */
.paragraph {
  font-style: oblique;
}
</style>
