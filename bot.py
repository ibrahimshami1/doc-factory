import os
import threading
import telebot
from flask import Flask

TOKEN = "8259880462:AAGhO3Y1xDDa9A4ygkt53l77u7--BDtqEUc"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا مدير المصنع. النظام السحابي على Render يعمل بنجاح تام وجاهز لاستقبال فكرة الوثائقي.")

@bot.message_handler(func=lambda message: True)
def generate_documentary_structure(message):
    idea = message.text
    bot.reply_to(message, f"⏳ جاري تحليل قضية '{idea}' وبناء الهيكل الوثائقي عبر المحرك السردي...")

    script_output = f"""
🎬 **تقرير المحرك السردي المبدئي:**
**عنوان الوثائقي:** {idea}

1️⃣ **الخطاف (The Hook - أول 30 ثانية):**
* مشهد صامت لـ كاميرا مراقبة (CCTV) تُظهر الساعة 02:14 صباحاً. صوت دقات ناعمة تزداد تدريجياً، يتبعها صوت تعليق صوتي منخفض: "في تلك الليلة، لم يكن أحد يعود كما كان.. ما حدث لم يكن مصادفة."

2️⃣ **الفصل الأول: البداية واللغز (Act I):**
* سرد تفاصيل ما قبل الحدث، تقديم الشخصيات أو المكان، وتأسيس التوتر النفسي.
* **إحداثيات الأرشيف البصري المقترحة:** لقطات شوارع قديمة، صور صحفية أرشيفية للحقبة الزمنية.

3️⃣ **الفصل الثاني: التحقيق والشكوك (Act II):**
* تفكيك الأدلة، ظهور الأدلة المتناقضة، وتصاعد حبكة الغموض.
* **إحداثيات الأرشيف البصري المقترحة:** لقطات محضر شرطة، وثائق رسمية مظلمة، لقطات مقربة (Close-up) لأدلة مادية.

4️⃣ **الفصل الثالث: الخاتمة واللغز المفتوح (Act III):**
* ترك المشاهد أمام السؤال الأكبر الذي لا إجابة قاطعة له، لتثبيت الأثر النفسي للوثائقي.

---
✅ **الحالة:** تم اكتمال بناء الهيكل السردي بنجاح على السحابة الدائمة!
    """
    bot.reply_to(message, script_output)

@app.route('/')
def home():
    return "Doc Factory Bot is running successfully!"

if __name__ == '__main__':
    def run_bot():
        bot.infinity_polling(skip_pending=True)
    
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
