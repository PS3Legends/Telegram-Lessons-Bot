import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

with open("lessons.json", "r", encoding="utf-8") as f:
    lessons = json.load(f)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name.upper(), callback_data=f"lang_{name}")] for name in lessons]
    await update.message.reply_text("اختر لغة البرمجة:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    if data.startswith("lang_"):
        lang = data.replace("lang_", "")
        user_data[uid] = {"lang": lang, "index": 0}
    elif data == "next":
        if uid in user_data:
            user_data[uid]["index"] += 1
        else:
            await query.edit_message_text("اكتب /start أولاً.")
            return
    else:
        return

    lang = user_data[uid]["lang"]
    index = user_data[uid]["index"]

    if lang not in lessons or index >= len(lessons[lang]):
        await query.edit_message_text("لا يوجد مزيد من الدروس.")
        return

    text = lessons[lang][index]["ar"]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("التالي", callback_data="next")]])
    await query.edit_message_text(f"{lang.upper()} - درس {index + 1}:\n{text}", reply_markup=reply_markup)

def main():
    app = Application.builder().token("YOUR_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()