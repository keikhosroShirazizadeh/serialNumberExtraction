from flask import Flask, request, jsonify
import os
from PIL import Image
from detectAndCropArea import detect_and_crop_object
from detection import extract_text_from_image
from detection2 import extract_pattern_text

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/serialDetection', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Optional: Open and process the image using Pillow
            image = Image.open(filepath)
            width, height = image.size

            template_path = 'template.jpg'
            output_path = './'+filename+'croppedcard.jpg'

            detect_and_crop_object(UPLOAD_FOLDER+"/"+filename,template_path,output_path)
            result=extract_text_from_image("serial.jpg")
            # result2=extract_pattern_text("serial.jpg")

            return jsonify({
                'message': 'File successfully uploaded',
                'filename': filename,
                'dimensions': {'width': width, 'height': height},
                'result':result
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error saving file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Image Upload API'}), 200

if __name__ == '__main__':
    app.run(debug=True)
