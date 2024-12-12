import together
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Thiết lập API key cho Together AI
together.api_key = "cf99c1a5c833e5c80bbe08376ed03bdea2e2e6be5a916808168fa35633603f0e"

# Khởi tạo client Together AI
client = together.Client()

@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        # Lấy mô tả từ yêu cầu
        data = request.json
        prompt = data.get("prompt")

        # Gọi API tạo ảnh từ Together AI
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=768,
            steps=4,
            n=1,
            response_format="b64_json"
        )

        # Lấy dữ liệu ảnh dưới dạng base64
        image_data = response.data[0].b64_json

        # Trả về dữ liệu ảnh dưới dạng JSON
        return jsonify({"image_base64": image_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)