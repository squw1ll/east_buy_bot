import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config (из переменных окружения) ──────────────────────────────
BOT_TOKEN = os.environ["BOT_TOKEN"]                       # токен от @BotFather
WEBAPP_URL = os.environ["WEBAPP_URL"]                      # https-ссылка на калькулятор (мини апп)
MANAGER_USERNAME = os.environ.get("MANAGER_USERNAME", "squw2ll")  # без @

WELCOME_TEXT = (
    "👋 Привет! Это <b>EastBuy_MD</b> — доставка товаров из Китая в Молдову.\n\n"
    "🧮 Нажми кнопку ниже, чтобы открыть калькулятор и посчитать стоимость "
    "доставки самолётом или кораблём.\n\n"
    "💬 Если остались вопросы — наш менеджер всегда на связи."
)


def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🧮 Открыть калькулятор", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("💬 Связаться с менеджером", url=f"https://t.me/{MANAGER_USERNAME}")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=build_keyboard(),
        parse_mode="HTML",
    )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Bot started, polling for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()