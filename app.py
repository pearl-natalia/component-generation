import base64
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Lock
from model import format_css

app = Flask(__name__)
CORS(app)
lock = Lock()

# reference.html
@app.route('/fetch-html', methods=['POST'])
def upload_component():
    if not lock.acquire(blocking=False):
        return jsonify({"message": "Server is busy. Please try again later."}), 503 

    try:
        data = request.json
        html_content = data.get('html')
        css_content = data.get('styles')

        with open("output/reference.html", "w") as file:
            file.write(f"{html_content}\n<style>\n{format_css(css_content)}\n</style>")

        print("Component saved. Running model.py...")
        result = subprocess.run(["python3", "model.py"], capture_output=True, text=True)

        return jsonify({"message": "Component received and processed!", "output": result.stdout}), 200

    finally:
        lock.release()

# reference.png
@app.route('/process-image', methods=['POST'])
def process_image():
    data = request.get_json()  
    image_data = data.get('image')

    if image_data:
        if image_data.startswith("data:image/png;base64,"):
            image_data = image_data.split(",")[1]

        try:
            image_binary = base64.b64decode(image_data)

            output_path = 'output/reference.png'

            with open(output_path, 'wb') as f:
                f.write(image_binary)

            return jsonify({"message": "Image received and processed", "path": output_path})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No image data provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
