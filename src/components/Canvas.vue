<template>
  <div class="mainwindow">
    <div class="content-row">
      <!-- Левая часть: рендер неба -->
      <div ref="container" class="three-container"></div>

      <!-- Правая часть: боковая панель -->
      <div class="sidebar">
        <img :src="`/illustrations/${image}`" class="constellation-icon" />
        <h2 class="constellation-title">{{name}}</h2>
        <div class="button-group">
          <Button title="Показать Маску" />
          <Button title="Следующее созвездие" />
        </div>
      </div>
    </div>

    <!-- Нижняя панель управления -->
    <div class="bottom-controls">
      <Button title="Загрузить другое" />
      <Button title="Сменить тему" />
      <Button title="Скачать" />
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, watch } from 'vue';
import * as THREE from 'three';
import Button from './MenuButton.vue';

const props = defineProps({
  imageSrc: String,
  points: Array,
  image: String,
  name: String,
});

const container = ref(null);
let scene, camera, renderer, imageMesh;
let lines = [];

let originalWidth = 0;
let originalHeight = 0;
let displayWidth = 0;
let displayHeight = 0;

const initThree = (width, height) => {
  scene = new THREE.Scene();

  camera = new THREE.OrthographicCamera(
      0, width, height, 0, 0.1, 1000
  );
  camera.position.z = 10;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setClearColor(0x000000, 1);

  container.value.innerHTML = '';
  container.value.appendChild(renderer.domElement);
};

const clearLines = () => {
  lines.forEach(line => {
    scene.remove(line);
    line.geometry.dispose();
    line.material.dispose();
  });
  lines = [];
};

const animateLineSegment = (start, end, material, delay = 600) => {
  return new Promise(resolve => {
    let progress = 0;
    const points = [start.clone(), start.clone()];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);
    scene.add(line);
    lines.push(line);

    const animateSegment = () => {
      progress += 0.01;
      if (progress >= 1) {
        geometry.setFromPoints([start, end]);
        resolve();
        return;
      }
      const current = start.clone().lerp(end, progress);
      geometry.setFromPoints([start, current]);
      requestAnimationFrame(animateSegment);
    };

    setTimeout(() => {
      animateSegment();
    }, delay);
  });
};

const scalePoints = () => {
  const scaleX = displayWidth / originalWidth;
  const scaleY = displayHeight / originalHeight;
  return props.points.map(p => {
    const x = p.x * scaleX;
    const y = p.y * scaleY;
    return new THREE.Vector3(x, displayHeight - y, 1);
  });
};

const drawLinesAnimated = async () => {
  if (!props.points || props.points.length < 2) return;

  clearLines();

  const material = new THREE.LineBasicMaterial({ color: '#FFF', linewidth: 2 });

  const scaledPoints = scalePoints();

  for (let i = 1; i < scaledPoints.length; i++) {
    await animateLineSegment(scaledPoints[i - 1], scaledPoints[i], material, 500);
  }
};

const loadAndDisplayImage = () => {
  const loader = new THREE.TextureLoader();
  loader.load(props.imageSrc, (texture) => {
    const img = texture.image;
    originalWidth = img.width;
    originalHeight = img.height;

    displayWidth = originalWidth;
    displayHeight = originalHeight;
    let isRotated = false;

    // Определяем нужно ли поворачивать (если изображение вертикальное)
    if (originalHeight > originalWidth) {
      isRotated = true;
      [displayWidth, displayHeight] = [originalHeight, originalWidth];
    }

    // Уменьшаем слишком широкие изображения
    if (displayWidth > 1000 && displayWidth > displayHeight) {
      const scaleFactor = 1000 / displayWidth;
      displayWidth = 1000;
      displayHeight = displayHeight * scaleFactor;
    }

    initThree(displayWidth, displayHeight);

    const geometry = new THREE.PlaneGeometry(displayWidth, displayHeight);
    const material = new THREE.MeshBasicMaterial({ map: texture });

    if (imageMesh) {
      scene.remove(imageMesh);
      imageMesh.geometry.dispose();
      imageMesh.material.dispose();
    }

    imageMesh = new THREE.Mesh(geometry, material);
    imageMesh.position.set(displayWidth / 2, displayHeight / 2, 0);

    if (isRotated) {
      imageMesh.rotation.z = Math.PI / 2;
    }

    scene.add(imageMesh);

    drawLinesAnimated();
    animate();
  });
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

const animate = () => {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
};
</script>

<style scoped>
.mainwindow {
  max-width: 1000px;
  margin: 80px 20px 0 20px;
  background: rgba(13, 17, 28, 0.8); /* полупрозрачный тёмный фон */
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5); /* мягкая тень */
  backdrop-filter: blur(12px); /* эффект стекла */
  border: 1px solid rgba(255, 255, 255, 0.05);
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
  overflow: hidden;
  padding: 10px;
}

.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #0a0a0a;
  border-radius: 12px;
  padding: 20px;
}

.constellation-icon {
  max-width: 220px;
  margin-bottom: 20px;
  height: 400px;
}

.constellation-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
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
