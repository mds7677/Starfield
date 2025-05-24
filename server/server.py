from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import traceback
from matcher import match

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

def get_next_filename(extension):
    counter = 1
    while True:
        filename = f"{counter}{extension}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(path):
            return filename, path
        counter += 1

def extract_coordinates(image_path):
    name, lines = match(image_path)
    return name, lines

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

        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({'error': f'Upload folder {UPLOAD_FOLDER} does not exist'}), 500

        if not os.access(UPLOAD_FOLDER, os.W_OK):
            return jsonify({'error': f'Upload folder {UPLOAD_FOLDER} is not writable'}), 500

        # Получаем расширение файла
        ext = os.path.splitext(file.filename)[1].lower()

        # Получаем следующее доступное имя файла
        filename, save_path = get_next_filename(ext)

        # Сохраняем файл
        file.save(save_path)
        print(f"Файл сохранён: {save_path}")

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


# call this function whereever you want:
#
# name, lines = match(import_path, export_path)
#
# name - short constellation name, such as UMi, Cep, etc
# lines - [[(x0, y0), (x1, y1)], [(x2, y2), (x3, y3)], ...]