from pyrogram import Client, filters
import datetime
import pytz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Youtube.config import Config
from Youtube.script import Translation
from Youtube.forcesub import handle_force_subscribe
from Youtube.db import add_user, get_all_users

# Set timezone to IST
ist = pytz.timezone('Asia/Kolkata')
currentTime = datetime.datetime.now(ist)

if currentTime.hour < 12:
    wish = "Good morning 🌞"
elif 12 <= currentTime.hour < 17:
    wish = "Good afternoon 🌤️"
else:
    wish = "Good evening 🌝"

@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()

@Client.on_message(filters.private & filters.command("about"))
async def about(client, message):
    if Config.CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return
    await message.reply_text(
        text=Translation.ABOUT_TXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('⛔️ Close', callback_data='cancel')]
            ]
        )
    )

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if Config.CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return

    add_user(message.from_user.id)

    await message.reply_photo(
        photo="https://graph.org/file/7af9a8ab33a563cc7e6d4.jpg",
        caption=Translation.START_TEXT.format(message.from_user.first_name, wish),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('📍 Update Channel', url='https://t.me/+055Dfay4AsNjYWE1')],
                [
                    InlineKeyboardButton('👩‍💻 Developer', url='https://t.me/fake_one'),
                    InlineKeyboardButton('👥 Support Group', url='https://t.me/+RrYHGxZqqX9lOGQ9'),
                ],
                [InlineKeyboardButton('⛔️ Close', callback_data='cancel')]
            ]
        )
    )

@Client.on_message(filters.command("help"))
def help(client, message):
    help_text = """
    Welcome to the YouTube Video Uploader Bot!

To upload a YouTube video, simply send me the YouTube link.
    
Enjoy using the bot!
    """
    message.reply_video(
        video="https://graph.org/file/b6841327d49e1699ff2ad.mp4",
        caption=help_text
    )

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast(client, message):
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("You are not authorized to use this command.")
        return

    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast it.")
        return

    reply_message = message.reply_to_message
    total_users = get_all_users().count()
    success_count = 0
    failed_count = 0
    blocked_count = 0

    for user in get_all_users():
        try:
            if reply_message.forward_from or reply_message.forward_from_chat:
                await client.forward_messages(chat_id=user['user_id'], from_chat_id=reply_message.chat.id, message_ids=reply_message.message_id)
            else:
                if reply_message.text:
                    await client.send_message(chat_id=user['user_id'], text=reply_message.text)
                elif reply_message.photo:
                    await client.send_photo(chat_id=user['user_id'], photo=reply_message.photo.file_id, caption=reply_message.caption)
                elif reply_message.video:
                    await client.send_video(chat_id=user['user_id'], video=reply_message.video.file_id, caption=reply_message.caption)
                elif reply_message.document:
                    await client.send_document(chat_id=user['user_id'], document=reply_message.document.file_id, caption=reply_message.caption)
                elif reply_message.audio:
                    await client.send_audio(chat_id=user['user_id'], audio=reply_message.audio.file_id, caption=reply_message.caption)
                elif reply_message.voice:
                    await client.send_voice(chat_id=user['user_id'], voice=reply_message.voice.file_id, caption=reply_message.caption)
                elif reply_message.sticker:
                    await client.send_sticker(chat_id=user['user_id'], sticker=reply_message.sticker.file_id)
                elif reply_message.animation:
                    await client.send_animation(chat_id=user['user_id'], animation=reply_message.animation.file_id, caption=reply_message.caption)
                elif reply_message.location:
                    await client.send_location(chat_id=user['user_id'], latitude=reply_message.location.latitude, longitude=reply_message.location.longitude)
                elif reply_message.contact:
                    await client.send_contact(chat_id=user['user_id'], phone_number=reply_message.contact.phone_number, first_name=reply_message.contact.first_name)
            
            success_count += 1
        except Exception as e:
            if "bot was blocked by the user" in str(e):
                blocked_count += 1
            else:
                failed_count += 1
            print(f"Failed to send message to {user['user_id']}: {e}")

    await message.reply_text(f"Broadcast completed.\nTotal users: {total_users}\nSuccess: {success_count}\nFailed: {failed_count}\nBlocked the bot: {blocked_count}")
