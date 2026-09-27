import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

load_dotenv()
TOKEN=os.getenv("BOT_TOKEN")
WEBAPP_URL=os.getenv("WEBAPP_URL")
if not TOKEN: raise RuntimeError("BOT_TOKEN не указан в .env")
if not WEBAPP_URL or not WEBAPP_URL.startswith("https://"):
    raise RuntimeError("WEBAPP_URL должен начинаться с https://")

dp=Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    kb=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇩🇪 Открыть Deutsch Lernen",
                              web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(
        "🇩🇪 <b>Deutsch Lernen</b>\n\n"
        "Изучай немецкие слова с картинками, примерами и повторением.",
        reply_markup=kb
    )

async def main():
    bot=Bot(TOKEN)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
