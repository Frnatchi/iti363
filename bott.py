import os
import telebot
from flask import Flask, request

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت الخاص بك
TOKEN = '8145006862:AAFWjlFMrOh0G7kQcpj2GtgMB-Ut8QxNoHU'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# تعريف مسار Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

# تعريف الأوامر ومعالجات الرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! 🎬 أرسل رابط فيديو TikTok وسأحمّله لك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    try:
        # إعداد خيارات التنزيل
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True
        }

        # تنزيل الفيديو
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو
        with open(filename, 'rb') as video_file:
            bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
                caption="تم التحميل بنجاح! ✅\n@YourBotName"
            )

        # حذف الملف المؤقت
        os.remove(filename)
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في التحميل: {str(e)}")

# تعيين Webhook عند تشغيل التطبيق
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://iti363.onrender.com/webhook')
    app.run(host='0.0.0.0', port=10000)
