import random
import discord
from discord.ext import commands
import os
import re

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=True)
bot.remove_command('help')

last_image_path = None  # Variable to store the path of the last image sent

@bot.event
async def on_message(message):
    global last_image_path  # Access the last_image_path variable

    if not message.author.bot:
        pattern1 = r"(?i)(?<!\S)(?!MeowFemBoy\b)(?:[-*_])?m(?:[-*_])?(?:\w(?:[-*_]))?e(?:[-*_])?(?:\w(?:[-*_]))?o(?:[-*_])?(?:\w(?:[-*_]))?w(?:[-*_])?\w*"
        pattern2 = r"(?i)\bMeowFemboy\b"

        if re.search(pattern1, message.content):
            if "bot" in message.channel.name.lower():
                folder_path = "/DiscordBots/Images/CatGirls"
                file_names = os.listdir(folder_path)
                image_paths = [
                    os.path.join(folder_path, file_name) for file_name in file_names
                ]
                if image_paths:
                    random_image_path = random.choice(image_paths)
                    with open(random_image_path, "rb") as image_file:
                        image = discord.File(image_file)
                        await message.channel.send(file=image)
                        last_image_path = random_image_path  # Store the path of the last image sent
                        print("Last image path:", last_image_path)
                else:
                    await message.channel.send("No images found.")
    
    await bot.process_commands(message)

@bot.command(name='killkitty')
async def killkitty(ctx):
    global last_image_path  # Access the last_image_path variable
    print("Got to Kill Command")
    if "bot" in ctx.channel.name.lower():
            print("Made it into first if")
            # Extract the filename from the path
            image_filename = os.path.basename(last_image_path)
            # Construct the full file path in the CatGirls folder
            catgirls_folder_path = "/DiscordBots/Images/CatGirls"
            image_file_path = os.path.join(catgirls_folder_path, image_filename)

            if os.path.exists(image_file_path):
                os.remove(image_file_path)  # Delete the image file from the CatGirls folder
                await ctx.send("Last image removed.")
                print("Attempted to delete:", last_image_path)
            else:
                await ctx.send("Last image file not found.")
    else:
        await ctx.send("No image to remove.")

bot.run(
  "")