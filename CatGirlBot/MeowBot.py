from b2sdk.v1 import B2Api, InMemoryAccountInfo
import random
import discord
from discord.ext import commands
import os
import re

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=True)
bot.remove_command('help')

last_image_path = None  # Variable to store the path of the last image sent

#Backblaze stuff
account_id = ""
application_key = ""
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", account_id, application_key)
bucket = b2_api.get_bucket_by_name("")


@bot.event
async def on_message(message):
    global last_image_path  # Access the last_image_path variable

    if not message.author.bot:
        pattern1 = r"(?i)\bMeow\b"
        pattern2 = r"(?i)\bFemboy\b"
        pattern3 = r"(?i)\bUwu\b"

    #Standard
        if re.search(pattern1, message.content):
            if "bot" in message.channel.name.lower():
                image_paths = []
                for file_version_info, folder_name in bucket.ls(folder_to_list='Meow'):
                    image_paths.append(file_version_info.file_name)
                if image_paths:
                    random_image_path = random.choice(image_paths)
                    await message.channel.send(b2_api.get_download_url_for_file_name(bucket_name="",file_name=random_image_path))
                    last_image_path = random_image_path  # Store the path of the last image sent
                    print("Last image path:", last_image_path)
                else:
                    await message.channel.send("No images found.")
  
    #With Dicks
        if re.search(pattern2, message.content):
            if "bot" in message.channel.name.lower():
                image_paths = []
                for file_version_info, folder_name in bucket.ls(folder_to_list='FemBoy'):
                    image_paths.append(file_version_info.file_name)
                if image_paths:
                    random_image_path = random.choice(image_paths)
                    await message.channel.send(b2_api.get_download_url_for_file_name(bucket_name="",file_name=random_image_path))
                    last_image_path = random_image_path  # Store the path of the last image sent
                    print("Last image path:", last_image_path)
                else:
                    await message.channel.send("No images found.")
    
    #Ff Degens   
        if re.search(pattern3, message.content):
            if "bot" in message.channel.name.lower():
                image_paths = []
                for file_version_info, folder_name in bucket.ls(folder_to_list='uwu'):
                    image_paths.append(file_version_info.file_name)
                if image_paths:
                    random_image_path = random.choice(image_paths)
                    await message.channel.send(b2_api.get_download_url_for_file_name(bucket_name="",file_name=random_image_path))
                    last_image_path = random_image_path  # Store the path of the last image sent
                    print("Last image path:", last_image_path)
                else:
                    await message.channel.send("No images found.")
    await bot.process_commands(message)
bot.run(
  "")
