import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Lock
from model import format_css

app = Flask(__name__)
CORS(app)
lock = Lock()

@app.route('/upload', methods=['POST'])
def upload_component():
    if not lock.acquire(blocking=False):
        return jsonify({"message": "Server is busy. Please try again later."}), 503  # Discard request if busy

    try:
        data = request.json
        html_content = data.get('html')
        css_content = data.get('styles')

        # Save the received component
        with open("output/reference.html", "w") as file:
            file.write(f"{html_content}\n<style>\n{format_css(css_content)}\n</style>")

        print("Component saved. Running model.py...")
        result = subprocess.run(["python3", "model.py"], capture_output=True, text=True)

        return jsonify({"message": "Component received and processed!", "output": result.stdout}), 200

    finally:
        lock.release()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
