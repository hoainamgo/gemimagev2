import together
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os

# Đọc biến môi trường từ file .env
load_dotenv()

# Thay thế bằng Token của bot Telegram của bạn
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Thiết lập API key cho Together AI
together.api_key = os.getenv("TOGETHER_API_KEY")

# Khởi tạo client Together AI
client = together.Client()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Chào mừng bạn đến với bot tạo ảnh! Gửi một mô tả để tạo ảnh.")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        # Gọi API tạo ảnh từ Together AI
        response = client.images.generate(
            prompt=user_message,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=768,
            steps=4,
            n=1,
            response_format="b64_json"
        )

        # Lấy dữ liệu ảnh dưới dạng base64
        image_data = response.data[0].b64_json

        # Chuyển đổi base64 thành ảnh
        image = Image.open(BytesIO(base64.b64decode(image_data)))

        # Lưu ảnh tạm thời
        image_file = BytesIO()
        image.save(image_file, format="PNG")
        image_file.seek(0)

        # Gửi ảnh về Telegram
        await update.message.reply_photo(photo=image_file)

    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra khi tạo ảnh: {e}")

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Bắt đầu bot
    application.run_polling()

if __name__ == "__main__":
    main()