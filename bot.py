import os
import threading
import telebot
from flask import Flask
from google import genai

# إعدادات التوكن ومفتاح الذكاء الاصطناعي (محدثة تلقائياً)
TELEGRAM_TOKEN = "8259880462:AAGhO3Y1xDDa9A4ygkt53l77u7--BDtqEUc"
GEMINI_API_KEY = "AQ.Ab8RN6JlGgVj3hwof3blOvmzgx1CVxCLUAkQU9gy2O6CIeGEuA"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# تهيئة عميل جوجل للذكاء الاصطناعي
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 أهلاً بك يا مدير المصنع. تم ربط النظام بنجاح بمحرك الذكاء الاصطناعي الحقيقي! أرسل لي الآن أي فكرة أو عنوان قضية جريمة وغموض لنكتب قصتها وسيناريوهاتها بالتفصيل.")

@bot.message_handler(func=lambda message: True)
def generate_ai_documentary(message):
    idea = message.text
    bot.reply_to(message, f"⏳ جاري الغوص في تفاصيل '{idea}' واستنطاق الملفات عبر محرك الذكاء الاصطناعي لتأليف القصة والسيناريو...")

    try:
        # صياغة الموجه (Prompt) للذكاء الاصطناعي ليكتب محتوى وثائقي مشوق
        prompt = f"""
        أنت كاتب وثائقيات جريمة وغموض محترف بأسلوب سينمائي مشوق.
        المطلوب كتابة هيكل وثائقي وقصة درامية مفصلة بناءً على العنوان التالي: "{idea}"
        
        اجعل الإجابة مرتبة وجاهزة للنشر والتسجيل الصوتي وتتضمن:
        1. عنوان مشوق ورئيسي.
        2. الخطاف (The Hook): أول 30 ثانية لجذب المشاهد بصوت منخفض ومشهد بصري غامض.
        3. تسلسل القصة والأحداث (الفصول الدرامية وتفكيك الأدلة).
        4. اقتراحات للأرشيف البصري والتعليق الصوتي.
        باللغة العربية وبأسلوب سردي احترافي.
        """

        # توليد المحتوى باستخدام نموذج gemini-2.5-flash السريع والذكي
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        script_output = response.text
        
        # تقسيم النص إذا كان طويلاً لكي لا يرفضه تليجرام
        if len(script_output) > 4000:
            chunks = [script_output[i:i+4000] for i in range(0, len(script_output), 4000)]
            for chunk in chunks:
                bot.send_message(message.chat.id, chunk)
        else:
            bot.reply_to(message, script_output)
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء التوليد عبر المحرك الذكي: {str(e)}")

@app.route('/')
def home():
    return "AI Doc Factory Bot is running and connected to Gemini!"

if __name__ == '__main__':
    def run_bot():
        bot.infinity_polling(skip_pending=True)
    
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
