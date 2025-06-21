import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json
import os
import random

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

YKS_DATE = datetime(2026, 6, 21, 10, 15)  # 21 Haziran 2026 10:15
ADMIN_ID = 6840212721
USER_FILE = "users.json"

# Motive edici sözler
MOTIVASYON_SOZLERI = [
    "Başarı, hazırlıklı olanlar içindir. Çalışmaya devam et!",
    "Hayallerinin peşinden gitmekten asla vazgeçme.",
    "Her gün bir adım daha ileri, sınav günü bir zafer daha yakın!",
    "Zorluklar geçicidir, başarı kalıcı.",
    "Sen inandığın sürece imkansız yoktur!",
    "Bugün attığın her adım, yarının başarısı olacak.",
    "Unutma, en güçlü rakibin dün yaptıklarındır.",
    "Azimle çalışanlar, her zaman kazanır.",
    "Sınav bir son değil, güzel başlangıçların kapısıdır.",
    "Yorulursan dinlen, ama vazgeçme!"
]

def save_user(user_id):
    users = set()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            try:
                users = set(json.load(f))
            except Exception:
                users = set()
    users.add(user_id)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f)

def get_all_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

async def sayac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    time_left = YKS_DATE - now
    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60

    motivasyon = random.choice(MOTIVASYON_SOZLERI)

    message = f"📚 YKS'ye Kalan Süre:\n\n"
    message += f"📅 {days} gün\n"
    message += f"⏰ {hours} saat\n"
    message += f"⌛ {minutes} dakika\n\n"
    message += f"{motivasyon}"

    await update.message.reply_text(message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    welcome_message = (
        "Merhaba! 👋\n\n"
        "YKS Sayaç botuna hoş geldiniz!\n"
        "Sınava kalan süreyi öğrenmek için /sayac komutunu kullanabilirsiniz.\n"
        "Başarılar! 📚✨"
    )
    await update.message.reply_text(welcome_message)

async def gonder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Bu komut sadece admin tarafından kullanılabilir.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("Lütfen göndermek istediğin mesajı yaz: /gonder <mesaj>")
        return
    mesaj = " ".join(args)

    users = get_all_users()
    sent_count = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=mesaj)
            sent_count += 1
        except Exception as e:
            logging.warning(f"{uid} kullanıcısına gönderilemedi: {e}")

    await update.message.reply_text(f"Toplam {sent_count} kullanıcıya mesaj gönderildi.")

def main():
    application = Application.builder().token('7642212104:AAGjoUsQnJd1F4jaEFrYbpH4VDbGIbVI1Uw').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sayac", sayac))
    application.add_handler(CommandHandler("gonder", gonder))

    application.run_polling()

if __name__ == '__main__':
    main()
