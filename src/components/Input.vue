<template>
  <div>
    <label class="custom-upload">
      Upload your file
      <input type="file" hidden @change="handleFileChange" />
    </label>
  </div>
</template>

<script>
export default {
  methods: {
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) {
        console.error('Файл не выбран');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:3000/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Ошибка при загрузке файла:', errorText);
          throw new Error('Ошибка при загрузке файла');
        }

        const result = await response.json();
        console.log('Файл успешно загружен:', result);
      } catch (error) {
        console.error('Ошибка при отправке файла:', error);
      }
    }
  }
}
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
  align-content: center;
  height: 70px;
  font-size: 30px;
  display: inline-block;
  max-width: 100%; /* Ограничивает ширину до 100% от контейнера */
  width: 100%; /* Ширина по контенту */
  box-sizing: border-box; /* Учитывает padding и border в ширине */
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
