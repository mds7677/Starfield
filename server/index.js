const express = require('express');
const multer = require('multer');
const cors = require('cors');

const app = express();
const upload = multer({ dest: 'uploads/' });x

app.use(cors());  // Разрешает CORS для всех источников

// Обработка POST-запроса для загрузки файла
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: 'Файл не был загружен' });
    }
    console.log('Получен файл:', req.file);
    res.json({ message: 'Файл загружен успешно', file: req.file });
});

app.listen(5173, () => {
    console.log('Сервер запущен на http://localhost:5173');
});
