import os
import telebot
import yt_dlp

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت الخاص بك
TOKEN = '8145006862:AAFWjlFMrOh0G7kQcpj2GtgMB-Ut8QxNoHU'
bot = telebot.TeleBot(TOKEN)

def is_valid_tiktok_url(url):
    """تحقق مما إذا كان الرابط صالحًا لـ TikTok"""
    domains = [
        'tiktok.com',
        'vm.tiktok.com',
        'vt.tiktok.com'
    ]
    return any(domain in url for domain in domains)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! 🎬 أرسل رابط فيديو TikTok وسأحمّله لك.")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text
    
    # التحقق من صحة الرابط أولاً
    if not is_valid_tiktok_url(url):
        bot.reply_to(message, "❌ الرابط غير صالح! يرجى إرسال رابط TikTok صحيح")
        return
        
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

if __name__ == '__main__':
    print("البوت يعمل...")
    bot.polling()
