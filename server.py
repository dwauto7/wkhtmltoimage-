from flask import Flask, request, send_file, jsonify
import subprocess, uuid, os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_image():
    html = request.json.get("html", "")
    if not html:
        return jsonify({"error": "Missing HTML"}), 400

    html_path = f"/tmp/{uuid.uuid4()}.html"
    image_path = f"/tmp/{uuid.uuid4()}.png"

    try:
        with open(html_path, "w") as f:
            f.write(html)

        result = subprocess.run(
            ["wkhtmltoimage", "--width", "600", html_path, image_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr.decode()}), 500

        return send_file(image_path, mimetype="image/png")

    finally:
        for path in [html_path, image_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
