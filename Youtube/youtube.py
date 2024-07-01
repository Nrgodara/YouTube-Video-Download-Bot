# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/YouTube-Video-Download-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot

import logging
import asyncio
import yt_dlp
from pyrogram import Client, filters
from Youtube.config import Config
from Youtube.forcesub import handle_force_subscribe


youtube_dl_username = None  
youtube_dl_password = None 

@Client.on_message(filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    if Config.CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    youtube_link = message.text
    try:
        downloading_msg = await message.reply_sticker("CAACAgUAAxkBAAIc8WZcSfIo-OOX3IT3eJ0h85aAyYnmAAKgDQACuMSRV7BENGrfZuYqNAQ")

        ydl_opts = {
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])]
        }

        if Config.HTTP_PROXY != "":
            ydl_opts['proxy'] = Config.HTTP_PROXY
        if youtube_dl_username is not None:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password is not None:
            ydl_opts['password'] = youtube_dl_password

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title', None)

            if title:
                ydl.download([youtube_link])
                uploading_msg = await message.reply_sticker("CAACAgUAAxkBAAIc62ZcR1mU5VRDVMUWh3iJuRcU3P0mAAKiAAPIlGQU_BpvPMzvnqw0BA")
                video_filename = f"downloaded_video_{info_dict['id']}.mp4"
                sent_message = await client.send_video(
                    message.chat.id,
                    video=open(video_filename, 'rb'),
                    caption=f"{title}\n\nDownloaded by: [YouTube Video Downloader Bot](https://t.me/ytdl_mbot)"
                )
    
    
    

                await asyncio.sleep(2)
                await downloading_msg.delete()
                await uploading_msg.delete()

                #await message.reply_text("\n\𝐎𝐰𝐧𝐞𝐫 : [𝑴𝑨𝑯𝑰®❤️‍🔥](https://t.me/+055Dfay4AsNjYWE1)\n\𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝!")
            else:
                logging.error("No video streams found.")
                await message.reply_text("Error: No downloadable video found.")
    except Exception as e:
        logging.exception("Error processing YouTube link: %s", e)
        await message.reply_text("Failed to process the YouTube link. Please try again later.\n\n**Error** : `e`")

# New command to download audio as MP3
@Client.on_message(filters.command(['song']))
async def download_audio(client, message):
    if Config.CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    youtube_link = message.text.split(' ', 1)[1]  # Extract the YouTube link from the message
    try:
        downloading_msg = await message.reply_sticker("CAACAgUAAxkBAAIc8WZcSfIo-OOX3IT3eJ0h85aAyYnmAAKgDQACuMSRV7BENGrfZuYqNAQ")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio_%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [lambda d: print(d['status'])]
        }

        if Config.HTTP_PROXY != "":
            ydl_opts['proxy'] = Config.HTTP_PROXY
        if youtube_dl_username is not None:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password is not None:
            ydl_opts['password'] = youtube_dl_password

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title', None)

            if title:
                ydl.download([youtube_link])
                audio_filename = f"downloaded_audio_{info_dict['id']}.mp3"
                uploading_msg = await message.reply_sticker("CAACAgUAAxkBAAIc62ZcR1mU5VRDVMUWh3iJuRcU3P0mAAKiAAPIlGQU_BpvPMzvnqw0BA")
                sent_message = await client.send_audio(
                    message.chat.id,
                    audio=open(audio_filename, 'rb'),
                    title=title,
                    caption=f"{title}\n\nDownloaded by: [YouTube Audio Downloader Bot](https://t.me/ytdl_mbot)"
                )

                await asyncio.sleep(2)
                await downloading_msg.delete()
                await uploading_msg.delete()

            else:
                logging.error("No audio streams found.")
                await message.reply_text("Error: No downloadable audio found.")
    except Exception as e:
        logging.exception("Error processing YouTube link: %s", e)
        await message.reply_text("Failed to process the YouTube link. Please try again later.\n\nError : e")
      
