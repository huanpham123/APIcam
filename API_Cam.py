from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)

# Thêm header cho phép CORS cho mọi request
@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    # Nếu dùng phương thức POST có thể cần header cho preflight:
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Dùng thư mục /tmp cho lưu trữ tạm thời (Vercel cho phép ghi dữ liệu vào /tmp)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Nếu bạn cần test giao diện riêng của Flask thì sử dụng file templates/camera.html.
    return render_template('camera.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Không có phần hình ảnh trong yêu cầu'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Chưa chọn file'}), 400

    filename = str(uuid.uuid4()) + '.jpg'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Tạo URL truy cập ảnh đã upload
    file_url = url_for('serve_upload', filename=filename, _external=True)
    return jsonify({'url': file_url})

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
