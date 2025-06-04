<template>
  <div class="mainwindow">
    <div class="content-row">
      <div ref="container" class="three-container"></div>
      <div class="sidebar">
        <img :src="`/illustrations/${name}.png`" class="constellation-icon"/>
        <h2 class="constellation-title">{{ name }}</h2>
        <div class="button-group">
          <Button title="Следующее созвездие"/>
        </div>
      </div>
    </div>
    <div class="bottom-controls">
      <Button @click="emitReload">
        <font-awesome-icon icon="file-arrow-down" />
        Загрузить другое
      </Button>
      <Button title="Сменить тему" />
      <Button @click="downloadImage">
        <font-awesome-icon icon="download" />
        Скачать изображение
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as THREE from 'three';
import Button from './MenuButton.vue';

const props = defineProps({
  imageSrc: String,
  points: Array,
  image: String,
  name: [String, Array],
});
const emit = defineEmits(['reload']);
const container = ref(null);

let scene, camera, renderer, imageMesh;
let lines = [];
let animationId = null;

function emitReload() {
  emit('reload');
}

function downloadImage() {
  if (!renderer || !scene || !camera) return;

  // Отрисовываем последний кадр (важно, если анимация была)
  renderer.render(scene, camera);

  const link = document.createElement('a');
  link.download = 'constellation.png';
  link.href = renderer.domElement.toDataURL('image/png');
  link.click();
}


function clearScene() {
  if (imageMesh) {
    scene.remove(imageMesh);
    imageMesh.geometry.dispose();
    imageMesh.material.dispose();
    imageMesh = null;
  }
  lines.forEach(({ line }) => {
    scene.remove(line);
    line.geometry.dispose();
    line.material.dispose();
  });
  lines = [];
}

function initThree(width, height) {
  scene = new THREE.Scene();
  camera = new THREE.OrthographicCamera(0, width, height, 0, 0.1, 1000);
  camera.position.z = 10;

  if (renderer) {
    renderer.dispose();
    if (renderer.domElement.parentNode) {
      renderer.domElement.parentNode.removeChild(renderer.domElement);
    }
  }

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setClearColor(0x000000, 1);

  if (container.value) {
    container.value.innerHTML = '';
    container.value.appendChild(renderer.domElement);
  }
}

function convertPoint(x, y, imgHeight, scaleFactor) {
  return new THREE.Vector3(x * scaleFactor, (imgHeight - y) * scaleFactor, 1);
}

function createLineGeometry(start, end, progress) {
  const currentPoint = start.clone().lerp(end, progress);
  return new THREE.BufferGeometry().setFromPoints([start, currentPoint]);
}

function setupLines(imgWidth, imgHeight, scaleFactor) {
  if (!props.points || !Array.isArray(props.points)) return;
  lines = [];

  const material = new THREE.LineBasicMaterial({ color: 0xffffff });

  props.points.forEach(pair => {
    if (Array.isArray(pair) && pair.length === 2) {
      const start = convertPoint(pair[0][0], pair[0][1], imgHeight, scaleFactor);
      const end = convertPoint(pair[1][0], pair[1][1], imgHeight, scaleFactor);
      const geometry = createLineGeometry(start, end, 0);
      const line = new THREE.Line(geometry, material);
      scene.add(line);
      lines.push({ line, start, end, progress: 0 });
    }
  });
}

function animate() {
  animationId = requestAnimationFrame(animate);
  const speed = 0.005;
  let allDone = true;

  lines.forEach(item => {
    if (item.progress < 1) {
      item.progress += speed;
      if (item.progress > 1) item.progress = 1;
      const newGeometry = createLineGeometry(item.start, item.end, item.progress);
      item.line.geometry.dispose();
      item.line.geometry = newGeometry;
      allDone = false;
    }
  });

  renderer.render(scene, camera);
  if (allDone) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
}

async function loadAndDisplayImage() {
  await nextTick();
  if (!container.value || !props.imageSrc) return;

  clearScene();

  const loader = new THREE.TextureLoader();
  loader.load(props.imageSrc, (texture) => {
    const img = texture.image;
    const originalWidth = img.width;
    const originalHeight = img.height;

    const containerWidth = container.value.clientWidth;
    const containerHeight = container.value.clientHeight;

    const scaleFactor = Math.min(containerWidth / originalWidth, containerHeight / originalHeight);

    const scaledWidth = originalWidth * scaleFactor;
    const scaledHeight = originalHeight * scaleFactor;

    initThree(scaledWidth, scaledHeight);
    camera.updateProjectionMatrix();

    const geometry = new THREE.PlaneGeometry(scaledWidth, scaledHeight);
    const material = new THREE.MeshBasicMaterial({ map: texture });

    imageMesh = new THREE.Mesh(geometry, material);
    imageMesh.position.set(scaledWidth / 2, scaledHeight / 2, 0);
    scene.add(imageMesh);

    setupLines(originalWidth, originalHeight, scaleFactor);

    if (animationId) cancelAnimationFrame(animationId);
    animate();
  });
}

watch(() => props.imageSrc, loadAndDisplayImage, { immediate: true });
watch(() => props.points, loadAndDisplayImage, { immediate: true });

onMounted(() => {
  if (props.imageSrc) loadAndDisplayImage();
});

onBeforeUnmount(() => {
  clearScene();
  if (animationId) cancelAnimationFrame(animationId);
  if (renderer) {
    renderer.dispose();
    if (renderer.domElement?.parentNode) {
      renderer.domElement.parentNode.removeChild(renderer.domElement);
    }
  }
});
</script>

<style scoped>
.mainwindow {
  max-width: 1400px;
  margin: 60px auto;
  padding: 30px;
  background: #050911;
  border-radius: 24px;
  border: 2px solid #131924;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-row {
  display: flex;
  flex-direction: row;
  gap: 40px;
  height: 700px;
}

.three-container {
  flex: 3;
  min-width: 0;
  height: 100%;
  max-width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
  border-radius: 12px;
  border: 2px solid #131924;
  overflow: hidden;
  position: relative;
}

.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #080d16;
  border-radius: 12px;
  border: 2px solid #131924;
  padding: 20px;
}

.constellation-icon {
  max-width: 220px;
  height: auto;
  margin-bottom: 20px;
}

.constellation-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  margin-top: auto;
}

.bottom-controls {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
