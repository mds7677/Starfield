from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Папка, куда будут сохраняться файлы
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_coordinates(image_path):
    # Заглушка — замени своей логикой
    return [(100, 200), (250, 300), (400, 100)]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part in the request'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    if not allowed_file(file.filename):
        return {'error': 'File type not allowed'}, 400

    filename = file.filename
    name, ext = os.path.splitext(filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    counter = 1
    while os.path.exists(save_path):
        filename = f"{name}_{counter}{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        counter += 1

    file.save(save_path)

    coordinates = extract_coordinates(save_path)

    return {
        'message': f'File saved to {save_path}',
        'filename': filename,
        'coordinates': coordinates
    }, 200

@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# from flask import Flask, request
# from flask_cors import CORS
# import os
#
# app = Flask(__name__)
# CORS(app)
#
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
# def extract_coordinates(image_path):
#     # Здесь будет твоя логика: нейросеть, OpenCV и т.п.
#     # Ниже — заглушка (возвращает фейковые координаты)
#     return [(100, 200), (250, 300), (400, 100)]
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return {'error': 'No file part in the request'}, 400
#
#     file = request.files['file']
#     if file.filename == '':
#         return {'error': 'No selected file'}, 400
#
#     filename = file.filename
#     name, ext = os.path.splitext(filename)
#     save_path = os.path.join(UPLOAD_FOLDER, filename)
#
#     counter = 1
#     while os.path.exists(save_path):
#         filename = f"{name}_{counter}{ext}"
#         save_path = os.path.join(UPLOAD_FOLDER, filename)
#         counter += 1
#
#     file.save(save_path)
#
#     coordinates = extract_coordinates(save_path)
#
#     return {
#         'message': f'File saved to {save_path}',
#         'filename': filename,
#         'coordinates': coordinates
#     }, 200
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# https://github.com/Stellarium/stellarium/tree/master/skycultures/modern/illustrations

# git@github.com:Stellarium/stellarium/tree/master/skycultures/modern/illustrations.git