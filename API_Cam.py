from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)

# Dùng thư mục /tmp cho lưu trữ tạm thời (vì hệ thống trên Vercel chỉ cho phép ghi dữ liệu vào /tmp)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Render giao diện HTML từ file templates/camera.html (nếu muốn sử dụng giao diện riêng trên Flask)
    return render_template('camera.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    # Kiểm tra file ảnh có trong request không
    if 'image' not in request.files:
        return jsonify({'error': 'Không có phần hình ảnh trong yêu cầu'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Chưa chọn file'}), 400

    # Sinh tên file ngẫu nhiên để tránh trùng lặp
    filename = str(uuid.uuid4()) + '.jpg'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Tạo URL để truy cập file đã lưu thông qua endpoint /uploads/<filename>
    file_url = url_for('serve_upload', filename=filename, _external=True)
    return jsonify({'url': file_url})

@app.route('/uploads/<filename>')
def serve_upload(filename):
    # Endpoint này trả file từ thư mục UPLOAD_FOLDER (/tmp/uploads)
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
