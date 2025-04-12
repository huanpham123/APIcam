from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh tĩnh
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cấu hình giới hạn kích thước file upload (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('camera.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    # Kiểm tra file ảnh có trong request không
    if 'image' not in request.files:
        return jsonify({'error': 'Không có phần hình ảnh trong yêu cầu'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Chưa chọn file'}), 400

    # Kiểm tra định dạng file
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return jsonify({'error': 'Chỉ chấp nhận file ảnh (JPEG, JPG, PNG)'}), 400

    try:
        # Sinh tên file ngẫu nhiên để tránh trùng lặp
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Tạo URL truy cập ảnh
        image_url = url_for('static', filename='uploads/' + filename, _external=True)
        return jsonify({'url': image_url})
    except Exception as e:
        return jsonify({'error': f'Lỗi khi xử lý ảnh: {str(e)}'}), 500

# For Vercel deployment
def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()(request)
        return response

if __name__ == '__main__':
    app.run(debug=True)
