from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import traceback
from matcher import match  # Твоя функция обработки

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        ext = os.path.splitext(file.filename)[1].lower()
        filename, save_path = get_next_filename(ext)

        file.save(save_path)
        print(f"Файл сохранён: {save_path}")

        # Вызов функции match на сохранённом изображении

        # ДОБАВИЛ ЛОГИ В str_log!!!!!!!!!!!!!
        try:
            name, lines, str_log = match(save_path)
            print(f"Обработка завершена: {name}, линии: {lines}")
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': f'Ошибка при обработке изображения: {str(e)}'}), 500

        return jsonify({
            'message': 'Файл успешно обработан',
            'filename': filename,
            'matched_name': name,
            'lines': lines
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
        return jsonify({'error': 'File not found error'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

