from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
CORS(app)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

# Убедимся, что папка существует
if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER)
        print(f"Создана папка для загрузок: {UPLOAD_FOLDER}")
    except Exception as e:
        print(f"Ошибка при создании папки {UPLOAD_FOLDER}: {e}")

# Разрешённые расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_coordinates(image_path):
    # Заглушка: здесь должна быть твоя логика анализа изображения
    return [(100, 200), (250, 300), (400, 100)]

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Проверяем доступность папки для записи
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({'error': f'Upload folder {UPLOAD_FOLDER} does not exist'}), 500

        if not os.access(UPLOAD_FOLDER, os.W_OK):
            return jsonify({'error': f'Upload folder {UPLOAD_FOLDER} is not writable'}), 500

        filename = file.filename
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        # Уникализация имени файла, если файл с таким именем уже есть
        counter = 1
        while os.path.exists(save_path):
            filename = f"{name}_{counter}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1

        # Логируем права и путь перед сохранением
        st = os.stat(UPLOAD_FOLDER)
        print(f"Upload folder permissions: {oct(st.st_mode)[-3:]}, path: {UPLOAD_FOLDER}")

        file.save(save_path)
        print(f"File saved to: {save_path}")

        # Проверяем файл после сохранения
        if not os.path.exists(save_path):
            return jsonify({'error': 'Failed to save file'}), 500

        coordinates = extract_coordinates(save_path)

        return jsonify({
            'message': f'File saved to {save_path}',
            'filename': filename,
            'coordinates': coordinates
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
