from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, make_response
import os
import uuid

app = Flask(__name__)

# Thêm header CORS cho mọi request để hỗ trợ Preflight (OPTIONS)
@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Thư mục lưu trữ tạm thời (Vercel cho phép ghi dữ liệu vào /tmp)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Nếu muốn test giao diện riêng của Flask
    return render_template('camera.html')

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_image():
    # Xử lý preflight request
    if request.method == 'OPTIONS':
        return '', 200

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
