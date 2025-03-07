import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton


TOKEN = "7972940517:AAFHegYVYhFtIw3G6SgVKF2pVtTujxYDbAk"
CHANNEL_USERNAME = "crax_tutorial"  # Kanal username (@siz yozing)
ADMIN_IDS = [6514551787]  # Admin IDlarini shu yerga qo‘ying

bot = telebot.TeleBot(TOKEN)
texts = {}  # Crax Top uchun saqlanadigan textlar


def check_subscription(user_id):
    """Foydalanuvchining kanalga obuna bo‘lganini tekshiradi."""
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        show_main_menu(message.chat.id)
    else:
        markup = InlineKeyboardMarkup()
        btn_channel = InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME}")
        btn_check = InlineKeyboardButton("✅ Tekshirish", callback_data="check_subscription")
        markup.add(btn_channel)
        markup.add(btn_check)

        bot.send_message(message.chat.id, "🔔 Botdan foydalanish uchun kanalga a'zo bo'ling!", reply_markup=markup)


def show_main_menu(chat_id):
    """Asosiy menyuni ko‘rsatadi."""
    markup = InlineKeyboardMarkup(row_width=2)

    # WebApp tugmalar
    buttons = [
        InlineKeyboardButton("🗂 chatGPT", web_app=WebAppInfo(url="https://chatgpt.com")),
        InlineKeyboardButton("✏️ Code Ai", web_app=WebAppInfo(url="https://zzzcode.ai")),
        InlineKeyboardButton("🛠 3D Text", web_app=WebAppInfo(url="https://panzoid.com")),
        InlineKeyboardButton("🗂 nakrutka", web_app=WebAppInfo(url="https://takipcimx.net")),
        InlineKeyboardButton("📥 Instagram", web_app=WebAppInfo(url="https://instagram.com")),
        InlineKeyboardButton("🔍 Grok", web_app=WebAppInfo(url="https://grok.com")),
    ]

    btn_crax_top = InlineKeyboardButton(f"📊 Rekga chiqish", callback_data="crax_top")

    markup.add(*buttons)
    markup.add(btn_crax_top)

    bot.send_message(chat_id, "📌 Asosiy menyu:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    """Foydalanuvchining obunasini tekshiradi."""
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Siz kanalga a'zo bo'lgansiz!")
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali kanalga a'zo bo'lmadingiz!", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "phone_name")
def phone_name_callback(call):
    """Telefon nomini olish uchun foydalanuvchidan kontakt so‘rash."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_contact = KeyboardButton("📱 Telefon nomini olish", request_contact=True)
    markup.add(btn_contact)

    bot.send_message(call.message.chat.id, "📲 Telefon modelini bilish uchun kontakt yuboring.", reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def get_phone_name(message):
    """Foydalanuvchi kontakt yuborganida telefon modelini chiqarish."""
    phone_number = message.contact.phone_number
    bot.send_message(message.chat.id, f"📱 Sizning telefoningiz: {phone_number}", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['panel'])
def admin_panel(message):
    """Faqat adminlar uchun panel."""
    if message.from_user.id in ADMIN_IDS:
        markup = InlineKeyboardMarkup()
        btn_add_text = InlineKeyboardButton("➕ Text qo‘shish", callback_data="add_text")
        markup.add(btn_add_text)
        bot.send_message(message.chat.id, "🔧 Admin Panel", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz!")
@bot.callback_query_handler(func=lambda call: call.data == "add_text")
def add_text(call):
    """Text qo‘shish jarayonini boshlash."""
    if call.from_user.id in ADMIN_IDS:
        bot.send_message(call.message.chat.id, "📝 Text nomini kiriting:")
        bot.register_next_step_handler(call.message, get_text_name)
    else:
        bot.answer_callback_query(call.id, "❌ Siz admin emassiz!", show_alert=True)


def get_text_name(message):
    """Text nomini olish."""
    text_name = message.text
    bot.send_message(message.chat.id, "✍️ Textni o‘zini kiriting:")
    bot.register_next_step_handler(message, lambda msg: save_text(msg, text_name))


def save_text(message, text_name):
    """Textni saqlash."""
    global texts
    text_content = message.text
    texts[text_name] = text_content

    markup = InlineKeyboardMarkup()
    btn_crax_top = InlineKeyboardButton(f"🔥 Crax Top ({len(texts)})", callback_data="crax_top")
    markup.add(btn_crax_top)

    bot.send_message(message.chat.id, f"✅ {text_name} qo‘shildi!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "crax_top")
def show_crax_top(call):
    """Crax Topdagi matnlarni chiqarish."""
    if texts:
        text_list = "\n\n".join([f"🔹 {name}: {content}" for name, content in texts.items()])
        bot.send_message(call.message.chat.id, f"🔥 Crax Top:\n\n{text_list}")
    else:
        bot.send_message(call.message.chat.id, "❌ Crax Top bo‘sh!")


bot.polling()