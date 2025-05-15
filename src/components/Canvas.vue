<template>
  <div ref="container" class="three-container"></div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import * as THREE from 'three';

const props = defineProps({
  imageSrc: String,
  points: Array
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
.three-container {
  display: flex;
  justify-content: center;
  align-self: center;
  margin-top: 30px;
  overflow: hidden;
}
canvas {
  display: block;
  max-width: 100%;
  height: auto;
}
</style>
