<template>

  <div>
    <label class="custom-upload">
      Upload your file
      <input type="file" hidden @change="handleFileChange" />
    </label>
  </div>
  <MyCanvas v-if="ShowCanvas"
                  :imageSrc="imageSrc"
                  :points="[
    { x: 100, y: 100 },
    { x: 200, y: 150 },
    { x: 300, y: 120 },
    { x: 400, y: 200 }
  ]"

/>
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
      points: [
        { x: 100, y: 100 },
        { x: 200, y: 150 },
        { x: 300, y: 120 },
        { x: 400, y: 200 }
      ], // координаты для векторов
    };
  },
  methods: {
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) {
        console.error('Файл не выбран');
        return;
      }

      this.ShowCanvas = true;

      const reader = new FileReader();
      reader.onload = () => {
        this.imageSrc = reader.result;
      };
      reader.readAsDataURL(file);
    },
  },
};
</script>

<style scoped>
.custom-upload {
  background-color: #60519b;
  box-shadow: 0 4px 8px 0 #bfc0d1;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  align-items: center;
  height: 70px;
  font-size: 30px;
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  opacity: 0;
  animation: fadeUp 1.3s ease-out forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
