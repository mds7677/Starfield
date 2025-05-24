<template>
  <div class="mainwindow">
    <div class="content-row">
      <div ref="container" class="three-container" />
      <div class="sidebar">
        <img :src="`/illustrations/${image}`" class="constellation-icon" />
        <h2 class="constellation-title">{{ name }}</h2>
        <div class="button-group">
          <Button title="Следующее созвездие" />
        </div>
      </div>
    </div>
    <div class="bottom-controls">
      <Button title="Загрузить другое" @click="emitReload" />
      <Button title="Сменить тему" />
      <Button title="Скачать" @click="downloadImage" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, nextTick } from 'vue';
import * as THREE from 'three';
import Button from './MenuButton.vue';

const props = defineProps({
  imageSrc: String,
  points: Array, // [[[x, y], [x, y]], ...]
  image: String,
  name: String,
});

const emit = defineEmits(['reload']);
const emitReload = () => emit('reload');

const container = ref(null);
let scene, camera, renderer, imageMesh;
let lines = [];

const initThree = (width, height) => {
  scene = new THREE.Scene();

  camera = new THREE.OrthographicCamera(0, width, height, 0, 0.1, 1000);
  camera.position.z = 10;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setClearColor(0x000000, 1);

  container.value.innerHTML = '';
  container.value.appendChild(renderer.domElement);
};

const clearScene = () => {
  if (imageMesh) {
    scene.remove(imageMesh);
    imageMesh.geometry.dispose();
    imageMesh.material.dispose();
    imageMesh = null;
  }

  lines.forEach(line => {
    scene.remove(line);
    line.geometry.dispose();
    line.material.dispose();
  });
  lines = [];
};

const drawLines = (scaleX, scaleY, imageHeight) => {
  if (!props.points || !Array.isArray(props.points)) return;

  const material = new THREE.LineBasicMaterial({ color: '#ffffff', linewidth: 2 });

  props.points.forEach(pair => {
    if (pair.length === 2) {
      const [start, end] = pair;
      const x1 = start.x * scaleX;
      const y1 = imageHeight - start.y * scaleY;
      const x2 = end.x * scaleX;
      const y2 = imageHeight - end.y * scaleY;

      const geometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(x1, y1, 1),
        new THREE.Vector3(x2, y2, 1),
      ]);
      const line = new THREE.Line(geometry, material);
      scene.add(line);
      lines.push(line);
    }
  });
};

const loadAndDisplayImage = async () => {
  await nextTick();

  // Получаем ширину контейнера для вписывания изображения по ширине
  const containerWidth = container.value.clientWidth;
  const containerHeight = container.value.clientHeight; // высота контейнера (можно использовать для ограничений)

  const loader = new THREE.TextureLoader();
  loader.load(props.imageSrc, texture => {
    clearScene();

    const img = texture.image;
    const imgWidth = img.width;
    const imgHeight = img.height;

    // Ограничиваем максимальную ширину рендера (например 1000)
    let renderWidth = imgWidth;
    let renderHeight = imgHeight;

    if (renderWidth > 1000) {
      const scaleFactor = 1000 / renderWidth;
      renderWidth = 1000;
      renderHeight = renderHeight * scaleFactor;
    }

    // Инициализируем сцену с размерами исходного изображения (ограниченного по ширине)
    initThree(renderWidth, renderHeight);

    // Масштаб для отрисовки так, чтобы картинка вписалась во всю ширину контейнера
    const scaleX = containerWidth / imgWidth;
    const scaleY = scaleX; // чтобы сохранить пропорции при масштабировании по ширине

    // Создаем геометрию и материал для плоскости изображения
    const geometry = new THREE.PlaneGeometry(renderWidth, renderHeight);
    const material = new THREE.MeshBasicMaterial({ map: texture });

    imageMesh = new THREE.Mesh(geometry, material);
    // Центрируем изображение
    imageMesh.position.set(renderWidth / 2, renderHeight / 2, 0);
    scene.add(imageMesh);

    // Рисуем линии с учетом масштаба (чтобы линии совпадали с масштабированным изображением)
    drawLines(scaleX, scaleY, renderHeight);

    animate();
  });
};


const animate = () => {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
};

const downloadImage = () => {
  renderer.render(scene, camera);
  const dataURL = renderer.domElement.toDataURL('image/png');

  const link = document.createElement('a');
  link.href = dataURL;
  link.download = `${props.name || 'constellation'}.png`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

watch(() => props.imageSrc, () => {
  if (props.imageSrc) {
    loadAndDisplayImage();
  }
});

onMounted(() => {
  if (props.imageSrc) {
    loadAndDisplayImage();
  }
});
</script>

<style scoped>
.mainwindow {
  max-width: 1000px;
  margin: 80px 20px 0 20px;
  background: #050911;
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  border: 2px solid #131924;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-row {
  display: flex;
  flex-direction: row;
  gap: 40px;
}

.three-container {
  flex: 3;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
  border-radius: 12px;
  border: 2px solid #131924;
  overflow: hidden;
  padding: 10px;
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
  margin-bottom: 20px;
  height: 350px;
}

.constellation-title {
  font-size: 24px;
  font-weight: bold;
  margin-top: 20px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.bottom-controls {
  display: flex;
  justify-content: space-between;
  padding: 20px 0;
}
</style>