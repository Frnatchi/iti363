import os
import telebot
import yt_dlp
from snapchat_dl import SnapchatDL

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت الخاص بك
TOKEN = '8145006862:AAFWjlFMrOh0G7kQcpj2GtgMB-Ut8QxNoHU'
bot = telebot.TeleBot(TOKEN)

def is_valid_url(url, platform):
    """تحقق من صحة الرابط بناءً على المنصة"""
    if platform == "tiktok":
        domains = ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
    elif platform == "youtube":
        domains = ['youtube.com', 'youtu.be']
    elif platform == "snapchat":
        domains = ['snapchat.com']
    else:
        return False
    return any(domain in url for domain in domains)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! 🎬 أرسل رابط فيديو TikTok أو YouTube أو صورة Snapchat وسأحاول تحميلها لك.")

@bot.message_handler(func=lambda m: True)
def download_content(message):
    url = message.text
    
    # تحديد المنصة بناءً على الرابط
    if is_valid_url(url, "tiktok"):
        download_tiktok(message)
    elif is_valid_url(url, "youtube"):
        download_youtube(message)
    elif is_valid_url(url, "snapchat"):
        download_snapchat(message)
    else:
        bot.reply_to(message, "❌ الرابط غير مدعوم! يرجى إرسال رابط TikTok أو YouTube أو Snapchat صحيح.")

def download_tiktok(message):
    url = message.text
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'tiktok_video.%(ext)s',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="تم تحميل الفيديو من TikTok بنجاح! ✅")

        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في تحميل الفيديو من TikTok: {str(e)}")

def download_youtube(message):
    url = message.text
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'youtube_video.%(ext)s',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="تم تحميل الفيديو من YouTube بنجاح! ✅")

        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في تحميل الفيديو من YouTube: {str(e)}")

def download_snapchat(message):
    url = message.text
    try:
        # تنزيل الصورة من Snapchat
        snap_dl = SnapchatDL()
        result = snap_dl.download(url)

        if result and os.path.exists(result['file_path']):
            with open(result['file_path'], 'rb') as photo_file:
                bot.send_photo(message.chat.id, photo_file, caption="تم تحميل الصورة من Snapchat بنجاح! ✅")
            os.remove(result['file_path'])
        else:
            bot.reply_to(message, "❌ لم يتم العثور على صورة في الرابط المقدم.")
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في تحميل الصورة من Snapchat: {str(e)}")

if __name__ == '__main__':
    print("البوت يعمل...")
    bot.polling()
