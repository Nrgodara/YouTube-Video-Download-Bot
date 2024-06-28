# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/YouTube-Video-Download-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot

import logging
import asyncio
import yt_dlp
from pyrogram import Client, filters
from Youtube.config import Config
from Youtube.forcesub import handle_force_subscribe
from pyrogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
import ffmpeg


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
        await message.reply_text("Failed to process the YouTube link. Please try again later.\n\nError : e")

@Client.on_message(filters.command("remix") & filters.private)
async def remix_command(client, message: Message):
    await message.reply(
        "Please send the audio file you want to remix.",
        quote=True
    )

@Client.on_message(filters.audio & filters.private)
async def handle_audio(client, message: Message):
    # Save the audio file for processing
    audio_file = await message.download()
    
    # Provide a menu for editing options
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("3D Audio", callback_data="effect_3d")],
        [InlineKeyboardButton("Bass Boost", callback_data="effect_bass_boost")],
        [InlineKeyboardButton("Echo", callback_data="effect_echo")],
        [InlineKeyboardButton("Tempo Change", callback_data="effect_tempo")],
        [InlineKeyboardButton("Reset Effects", callback_data="effect_reset")]
    ])
    
    await message.reply(
        "Select the effect you want to apply to your audio:",
        reply_markup=markup,
        quote=True
    )
    
    # Store the audio file path in user data (you can use a dictionary or a database)
    client.user_data[message.from_user.id] = audio_file


@Client.on_callback_query(filters.regex(r"^effect_"))
async def apply_effect(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    effect = callback_query.data.split("_")[1]
    audio_file = client.user_data.get(user_id)
    
    if not audio_file:
        await callback_query.message.edit_text("No audio file found. Please send an audio file first using /remix.")
        return
    
    output_file = f"remixed_{os.path.basename(audio_file)}"
    
    # Apply the selected effect using FFmpeg
    if effect == "3d":
        ffmpeg_cmd = f"ffmpeg -i {audio_file} -filter_complex \"apulsator=hz=0.1\" {output_file}"
    elif effect == "bass_boost":
        ffmpeg_cmd = f"ffmpeg -i {audio_file} -af \"bass=g=20\" {output_file}"
    elif effect == "echo":
        ffmpeg_cmd = f"ffmpeg -i {audio_file} -af \"aecho=0.8:0.88:60:0.4\" {output_file}"
    elif effect == "tempo":
        ffmpeg_cmd = f"ffmpeg -i {audio_file} -filter:a \"atempo=1.25\" {output_file}"
    elif effect == "reset":
        # Reset to the original audio
        output_file = audio_file
        await callback_query.message.reply_audio(audio=audio_file, caption="Original audio restored.")
        return
    
    # Execute the FFmpeg command
    os.system(ffmpeg_cmd)
    
    # Send the remixed audio back to the user
    await callback_query.message.reply_audio(
        audio=output_file,
        caption=f"Here is your audio with {effect.replace('_', ' ').capitalize()} effect.",
        title="Remixed Audio"
    )
    
    # Optionally, send the remixed audio to the log channel
    
    await client.send_audio(
        chat_id= "-1002078217156",
        audio=output_file,
        caption=f"Remixed audio with {effect.replace('_', ' ').capitalize()} effect by [{callback_query.from_user.first_name}](tg://user?id={user_id})",
        title="Remixed Audio"
    )
    
    # Clean up
    if os.path.exists(output_file) and output_file != audio_file:
        os.remove(output_file)
      
