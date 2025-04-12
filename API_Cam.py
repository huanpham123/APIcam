from flask import Flask, render_template, request, jsonify
from io import BytesIO
import uuid
import base64

app = Flask(__name__)

# We'll store images in memory (not suitable for production)
image_storage = {}

@app.route('/')
def index():
    return render_template('camera.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Generate unique ID for the image
        image_id = str(uuid.uuid4())
        
        # Read the file into memory
        image_data = file.read()
        
        # Store in memory (base64 encoded for simplicity)
        image_storage[image_id] = {
            'data': base64.b64encode(image_data).decode('utf-8'),
            'content_type': file.content_type
        }
        
        # Return URL to access the image
        image_url = url_for('get_image', image_id=image_id, _external=True)
        return jsonify({'url': image_url})
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/image/<image_id>')
def get_image(image_id):
    if image_id not in image_storage:
        return "Image not found", 404
        
    image_data = base64.b64decode(image_storage[image_id]['data'])
    return app.response_class(image_data, mimetype=image_storage[image_id]['content_type'])

# For Vercel
def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()(request)
        return response

if __name__ == '__main__':
    app.run(debug=True)
