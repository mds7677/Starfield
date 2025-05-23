<template>
  <div ref="sceneContainer" class="starfield"></div>
</template>

<script setup>
import * as THREE from 'three'
import { onMounted, ref } from 'vue'
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";

const sceneContainer = ref(null)

onMounted(() => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 2000)
  camera.position.z = 15

  const renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 1)
  sceneContainer.value.appendChild(renderer.domElement)

  // ЗВЕЗДЫ
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
    transparent: true,
    opacity: 0.8
  })

  const stars = new THREE.Points(starGeometry, starMaterial)
  const starGroup = new THREE.Group()
  starGroup.add(stars)
  scene.add(starGroup)

  // BLOOM
  const renderScene = new RenderPass(scene, camera)
  const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.3, 0.6, 0.15)
  bloomPass.threshold = 0.08
  bloomPass.strength = 1.4
  bloomPass.radius = 0.8

  const bloomComposer = new EffectComposer(renderer)
  bloomComposer.setSize(window.innerWidth, window.innerHeight)
  bloomComposer.renderToScreen = true
  bloomComposer.addPass(renderScene)
  bloomComposer.addPass(bloomPass)

  // ЗЕМЛЯ
  const earthGroup = new THREE.Group()

  const textureLoader = new THREE.TextureLoader()
  const dayMap = textureLoader.load('8k_earth_daymap.jpg')
  const nightMap = textureLoader.load('8k_earth_nightmap.jpg')
  const normalMap = textureLoader.load('/8k_earth_normal_map.tif')
  const specularMap = textureLoader.load('8k_earth_specular_map.tif')
  const cloudMap = textureLoader.load('8k_earth_clouds.jpg')

  const earthGeometry = new THREE.SphereGeometry(7.5, 64, 64)
  const earthMaterial = new THREE.MeshStandardMaterial({
    map: dayMap,
    normalMap: normalMap,
    normalScale: new THREE.Vector2(1.5, 1.5),
    roughness: 0.6,
    metalness: 0.2,
    specularMap: specularMap,
    emissive: 0x002244,
    emissiveIntensity: 0.15,
    envMapIntensity: 0.3,
  })

  const earth = new THREE.Mesh(earthGeometry, earthMaterial)
  earthGroup.position.set(0, -1, 0)
  earthGroup.add(earth)

  // Облака
  const cloudGeometry = new THREE.SphereGeometry(7.55, 64, 64)
  const cloudMaterial = new THREE.MeshPhongMaterial({
    map: cloudMap,
    transparent: true,
    opacity: 0.4,
    depthWrite: false,
    shininess: 25,
  })
  const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial)
  earthGroup.add(clouds)

  // Ночная сторона
  const nightMaterial = new THREE.MeshBasicMaterial({
    map: nightMap,
    blending: THREE.AdditiveBlending,
    side: THREE.FrontSide,
    transparent: true,
    opacity: 0.55
  })
  const nightLayer = new THREE.Mesh(earthGeometry.clone(), nightMaterial)
  earthGroup.add(nightLayer)

  // Атмосфера
  const atmosphereGeometry = new THREE.SphereGeometry(7.6, 64, 64)
  const atmosphereMaterial = new THREE.MeshBasicMaterial({
    color: 0x3399ff,
    transparent: true,
    opacity: 0.07,
    side: THREE.BackSide
  })
  const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial)
  earthGroup.add(atmosphere)

  scene.add(earthGroup)

  // СОЛНЦЕ
  const sunGroup = new THREE.Group()
  textureLoader.load('8k_sun.jpg', (sunTexture) => {
    const sunGeometry = new THREE.SphereGeometry(4, 64, 64)
    const sunMaterial = new THREE.MeshStandardMaterial({
      map: sunTexture,
      emissive: 0xffff33,
      emissiveIntensity: 1.6,
      metalness: 0.3,
      roughness: 1.2,
    })

    const sun = new THREE.Mesh(sunGeometry, sunMaterial)
    const light = new THREE.PointLight(0xffee88, 2.0, 300)
    light.position.set(0, 0, 0)
    sun.add(light)
    sun.position.set(0, 30, -200)
    sunGroup.add(sun)
    scene.add(sunGroup)
  })

  // ОБЩИЙ СВЕТ
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  // АНИМАЦИЯ
  const animate = () => {
    requestAnimationFrame(animate)

    starGroup.rotation.y += 0.0004
    earth.rotation.y += 0.001
    clouds.rotation.y += 0.0012
    nightLayer.rotation.y += 0.001
    sunGroup.rotation.y += 0.0008
    bloomComposer.render()
  }

  animate()

  // РЕЗАЙЗ
  window.addEventListener('resize', () => {
    const width = window.innerWidth
    const height = window.innerHeight
    camera.aspect = width / height
    camera.updateProjectionMatrix()
    renderer.setSize(width, height)
    bloomComposer.setSize(width, height)
  })
})
</script>

<style scoped>
.starfield {
  width: 100vw;
  height: 520px;
  position: relative;
  overflow: hidden;
  background-color: black;
}
</style>
