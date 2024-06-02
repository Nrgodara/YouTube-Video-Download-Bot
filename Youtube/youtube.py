import logging
import asyncio
import yt_dlp
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Youtube.config import Config
from Youtube.forcesub import handle_force_subscribe

youtube_dl_username = None  
youtube_dl_password = None 

formats_dict = {}

@Client.on_message(filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    if Config.CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return

    youtube_link = message.text
    try:
        downloading_msg = await message.reply_text("☄️")

        ydl_opts = {
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])]
        }

        if Config.HTTP_PROXY:
            ydl_opts['proxy'] = Config.HTTP_PROXY
        if youtube_dl_username:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password:
            ydl_opts['password'] = youtube_dl_password

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title')
            thumbnail_url = info_dict.get('thumbnail')
            formats = info_dict.get('formats', [])

            if title:
                buttons = []
                for fmt in formats:
                    if 'height' in fmt:
                        height = fmt.get('height', 'Unknown')
                        filesize_mb = fmt.get('filesize', 0) / (1024 * 1024) if fmt.get('filesize') else 'Unknown'
                        button_text = f"{height}p - {filesize_mb:.2f} MB" if filesize_mb != 'Unknown' else f"{height}p - Unknown size"
                        callback_data = f"{info_dict['id']}|{fmt['format_id']}"
                        buttons.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

                formats_dict[info_dict['id']] = {
                    'youtube_link': youtube_link,
                    'thumbnail_url': thumbnail_url,
                    'title': title
                }

                await message.reply_text(
                    "Choose the quality to download:",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                await downloading_msg.delete()
            else:
                logging.error("No video streams found.")
                await message.reply_text("Error: No downloadable video found.")
                await downloading_msg.delete()
    except Exception as e:
        logging.exception("Error processing YouTube link: %s", e)
        await message.reply_text(f"Failed to process the YouTube link. Please try again later.\n\nError: {e}")
        await downloading_msg.delete()

@Client.on_callback_query()
async def callback_query_handler(client, callback_query: CallbackQuery):
    try:
        data = callback_query.data.split('|')
        video_id = data[0]
        format_id = data[1]
        video_info = formats_dict.get(video_id)

        if not video_info:
            await callback_query.message.edit_text("Error: Invalid video ID.")
            return

        youtube_link = video_info['youtube_link']
        thumbnail_url = video_info['thumbnail_url']
        title = video_info['title']

        ydl_opts = {
            'format': format_id,
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])]
        }

        if Config.HTTP_PROXY:
            ydl_opts['proxy'] = Config.HTTP_PROXY
        if youtube_dl_username:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password:
            ydl_opts['password'] = youtube_dl_password

        downloading_msg = await callback_query.message.reply_sticker("CAACAgUAAxkBAAIc62ZcR1mU5VRDVMUWh3iJuRcU3P0mAAKiAAPIlGQU_BpvPMzvnqw0BA")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=True)
            video_filename = ydl.prepare_filename(info_dict)

        thumbnail_filename = "thumbnail.jpg"
        response = requests.get(thumbnail_url)
        with open(thumbnail_filename, 'wb') as f:
            f.write(response.content)

        with open(video_filename, 'rb') as video_file:
            await client.send_video(
                callback_query.message.chat.id,
                video=video_file,
                caption=f"{title}\n\nDownloaded by: [YouTube Video Downloader Bot](https://t.me/ytdl_mbot)",
                thumb=thumbnail_filename
            )

        await downloading_msg.delete()
        await callback_query.message.delete()
        
    except Exception as e:
        logging.exception("Error downloading YouTube video: %s", e)
        await callback_query.message.reply_text(f"Failed to download the video. Please try again later.\n\nError: {e}")

if __name__ == "__main__":
    app = Client("youtube_downloader", config=Config)
    app.run()
