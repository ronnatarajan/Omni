from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image_data = request.get_json()
        image_b64 = image_data['image']
        image = Image.open(BytesIO(base64.b64decode(image_b64)))

        # Process the image (e.g., save, analyze, etc.)
        image.save("received_image.png")

        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)