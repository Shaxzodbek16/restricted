from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from telethon import TelegramClient
from app.core.settings.config import Settings, get_settings
import re
import os

# Sozlamalar
settings: Settings = get_settings()

router = Router()
bot = Bot(token=settings.BOT_TOKEN)
client = TelegramClient("session", settings.API_ID, settings.API_HASH)


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "Hello! Send me a private channel link, and I'll fetch the message for you."
    )


@router.message(F.text.startswith("https://t.me/c/"))
async def handle_link(message: Message):
    link = message.text

    match = re.search(r"https://t\.me/c/(\d+)/(\d+)", link)
    if not match:
        await message.answer("❌ Xato! To'g'ri formatda link yuboring.")
        return

    chat_id, message_id = match.groups()
    chat_id = int(f"-100{chat_id}")  # Private kanallar uchun -100 qo'shiladi
    message_id = int(message_id)

    await message.answer("🔄 Xabar olinmoqda, biroz kuting...")

    try:
        async with client:
            msg = await client.get_messages(chat_id, ids=message_id)

            if msg:
                if msg.text:
                    await message.answer(f"📩 Xabar matni:\n\n{msg.text}")
                elif msg.photo:
                    photo_path = f"downloads/{message_id}.jpg"
                    await msg.download_media(photo_path)
                    await bot.send_photo(
                        message.chat.id, FSInputFile(photo_path), caption="📷 Rasm:"
                    )
                    os.remove(photo_path)  # Faylni o'chirish
                elif msg.video or msg.document:
                    video_path = f"downloads/{message_id}.mp4"
                    await msg.download_media(video_path)
                    await bot.send_video(
                        message.chat.id, FSInputFile(video_path), caption="🎥 Video:"
                    )
                    os.remove(video_path)  # Faylni o'chirish
                else:
                    await message.answer("⚠ Xabar matni yoki media mavjud emas.")
            else:
                await message.answer("❌ Xabar topilmadi!")

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
