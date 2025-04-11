from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    images = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    image_urls = [f"/static/uploads/{img}" for img in images]
    return render_template("camera.html", images=image_urls)

@app.route("/upload", methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({"success": False, "error": "Empty filename"}), 400

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    image_url = f"/static/uploads/{filename}"
    return jsonify({"success": True, "image_url": image_url})

@app.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
