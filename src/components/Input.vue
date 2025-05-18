<template>
  <div class="container">
    <label class="upload-label" for="fileInput" v-if="Visible">
      <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon-upload"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
      >
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M12 12V4m0 0l-4 4m4-4l4 4"
        />
      </svg>
      <span class="label-title">Загрузите изображение неба</span>
      <span class="label-subtitle">Мы определим созвездия на вашем небе</span>
      <input
          type="file"
          id="fileInput"
          class="hidden"
          @change="handleFileChange"
      />
    </label>

    <MyCanvas
        v-if="ShowCanvas"
        :imageSrc="imageSrc"
        :points="points"
        :image="Constellationsimage"
        :name = "constellationname"
    />
  </div>
</template>

<script>
import MyCanvas from "./Canvas.vue";
export default {
  components: {
    MyCanvas,
  },
  data() {
    return {
      ShowCanvas: false,
      imageSrc: null,
      Visible: true,
      Constellationsimage:null,
      constellationname:null,
      points: [
        { x: 100, y: 100 },
        { x: 200, y: 150 },
        { x: 300, y: 120 },
        { x: 400, y: 200 },
      ],
    };
  },
  methods: {
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.ShowCanvas = true;
      this.Visible = false;

      const reader = new FileReader();
      reader.onload = () => {
        this.imageSrc = reader.result;
      };
      reader.readAsDataURL(file);

      const formData = new FormData();
      formData.append("file", file);
      try {
        const res = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });
        if (!res.ok) throw new Error("Ошибка запроса");
        const data = await res.json();
        this.Constellationsimage.value=data.name
        this.constellationname=data.name;
        console.log("Загружено:", data);
      } catch (e) {
        console.error("Ошибка загрузки:", e);
      }
    },
  },
};
</script>

<style scoped>
.container {
  width: 800px;
  margin-top: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  align-self: center;
  height: 600px;
}

/* остальные стили без изменений */
@import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap");

.upload-label {
  font-family: 'Orbitron', sans-serif;
  width: 100%;
  align-content: center;
  height: 100%;
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  text-align: center;
  padding: 20px;
  background: radial-gradient(ellipse at bottom, #0a0f1c 0%, #000000 100%);
  background-size: cover;
  transition: all 0.3s ease;
  animation: fadeUp 1.3s ease-out forwards;
}

.upload-label::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url('./Stars/grain.png');
  opacity: 0.05;
  pointer-events: none;
  z-index: 1;
}

.upload-label:hover {
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}

.icon-upload {
  width: 48px;
  height: 48px;
  stroke: white;
  opacity: 0.6;
  margin-bottom: 10px;
  z-index: 2;
}

.label-title {
  font-size: 20px;
  font-weight: 600;
  z-index: 2;
}

.label-subtitle {
  font-size: 14px;
  opacity: 0.5;
  z-index: 2;
}

.hidden {
  display: none;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>