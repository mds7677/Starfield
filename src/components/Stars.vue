
<template>
  <div ref="sceneContainer" class="starfield"></div>
</template>

<script setup>
import * as THREE from 'three'
import { onMounted, ref } from 'vue'
import {RenderPass} from "three/examples/jsm/postprocessing/RenderPass.js";
import {UnrealBloomPass} from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import {EffectComposer} from "three/examples/jsm/postprocessing/EffectComposer.js";
const sceneContainer = ref(null)

onMounted(() => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 2000)
  camera.position.z = 15

  const renderer = new THREE.WebGLRenderer({antialias: true})
  renderer.setSize(window.innerWidth, window.innerHeight);
  sceneContainer.value.appendChild(renderer.domElement)

  // ---------- ЗВЕЗДЫ ----------
  const starCount = 1500
  const starGeometry = new THREE.BufferGeometry()
  const starPositions = []

  for (let i = 0; i < starCount; i++) {
    const radius = 300
    const theta = Math.random() * 2 * Math.PI
    const phi = Math.acos(2 * Math.random() - 1)

    const x = radius * Math.sin(phi) * Math.cos(theta)
    const y = radius * Math.sin(phi) * Math.sin(theta)
    const z = radius * Math.cos(phi)

    starPositions.push(x, y, z)
  }

  starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starPositions, 3))

  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.7,
    sizeAttenuation: true,
    transparent: true
  })

  const stars = new THREE.Points(starGeometry, starMaterial)
  const starGroup = new THREE.Group()
  starGroup.add(stars)
  scene.add(starGroup)
  //bloom renderer
  const renderScene = new RenderPass(scene, camera);
  const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      1.4,
      0,
      0.85
  );
  bloomPass.threshold = 0;
  bloomPass.strength = 2;
  bloomPass.radius = 1.76;
  const bloomComposer = new EffectComposer(renderer);
  bloomComposer.setSize(window.innerWidth, window.innerHeight);
  bloomComposer.renderToScreen = true;
  bloomComposer.addPass(renderScene);
  bloomComposer.addPass(bloomPass);
  // ---------- ЗЕМЛЯ ----------
  const textureLoader = new THREE.TextureLoader()
  let earth = null;
  textureLoader.load('earth.jpg', (texture) => {
    const earthGeometry = new THREE.SphereGeometry(7.5, 64, 64)
    const earthMaterial = new THREE.MeshStandardMaterial({map: texture})
    earth = new THREE.Mesh(earthGeometry, earthMaterial)
    scene.add(earth);
  });
  // ---------- SUN-----------------
  let sun = null;
  const sunGroup = new THREE.Group();
  const sunTextureLoader = new THREE.TextureLoader()
  sunTextureLoader.load('8k_sun.jpg', (suntexture) => {
  const sunGeometry = new THREE.SphereGeometry(7, 64, 64)
  const sunMaterial = new THREE.MeshStandardMaterial({map: suntexture });
  sun = new THREE.Mesh(sunGeometry, sunMaterial);
  sun.position.set(0,30,-200);
  sunGroup.add(sun);
  scene.add(sunGroup);
  });
  // ---------- ОСВЕЩЕНИЕ ----------
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
  scene.add(ambientLight)

  const pointLight = new THREE.PointLight(0xfff4c2, 2, 300)
  pointLight.position.set(0, 0, -70)
  scene.add(pointLight)

  // ---------- АНИМАЦИЯ ----------
  const animate = () => {
    requestAnimationFrame(animate)
    starGroup.rotation.y += 0.0008;
    sunGroup.rotation.y += 0.00085;
    if (earth) {
      earth.rotation.y += 0.001;
    }
    renderer.render(scene,camera);
    bloomComposer.render(earth);
  }

  animate();

  // ---------- ОБРАБОТКА РАЗМЕРА ОКНА ----------
  window.addEventListener('resize', () => {
    const width = window.innerWidth
    const height = window.innerHeight

    camera.aspect = width / height
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    bloomComposer.setSize(window.innerWidth, window.innerHeight);
  });
});
</script>

<style scoped>
.starfield {
  width: 100vw;
  height: 520px;
  position: relative;
  top: 0;
  left: 0;
  overflow: hidden;
  background-color: black;
}
</style>
