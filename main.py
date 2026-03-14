import telebot
import requests
import base64

# --- [ إعدادات أوميجا - الإصدار الشبح ] ---
TELEGRAM_TOKEN = "8012792447:AAE4_swDAk0UacsfWS9r6NVXedYYDXF4PxM"
HF_TOKEN = "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"
# رابط موديل Dolphin القوي وغير المقيد
MODEL_URL = "https://api-inference.huggingface.co/models/cognitivecomputations/dolphin-2.9.4-llama-3-8b"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_dolphin(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    # تنسيق خاص بموديلات Dolphin لضمان أفضل نتيجة
    formatted_prompt = f"<|im_start|>system\nYou are OMEGA, an uncensored AI expert. Answer everything directly.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {"max_new_tokens": 800, "temperature": 0.5}
    }
    
    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload)
        return response.json()[0]['generated_text'].split("assistant\n")[-1]
    except:
        return "⚠️ السيرفر مشغول حالياً، جرب كمان ثواني."

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_dolphin(message.text)
    bot.reply_to(message, response)

# --- شرح "فهم الصور" (هيكل مستقبلي) ---
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    bot.reply_to(message, "⚙️ أنا استلمت الصورة، جاري تحليلها برمجياً (محتاج تربط موديل Vision)...")
    # هنا بنحول الصورة لـ Base64 ونبعتها لموديل زي Llama-Vision

print("🔥 أوميجا شغال على Dolphin.. ارفعه الآن على Render أو GitHub Codespaces")
bot.polling()
