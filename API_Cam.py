from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh tĩnh (sẽ lưu vào thư mục static/uploads)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Render trang HTML có form upload
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

    # Tạo URL truy cập ảnh (sử dụng _external=True để trả về đường dẫn đầy đủ)
    image_url = url_for('static', filename='uploads/' + filename, _external=True)
    return jsonify({'url': image_url})

if __name__ == '__main__':
    app.run(debug=True)
