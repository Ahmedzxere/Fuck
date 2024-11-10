import discord
import joblib
from discord.ext import commands
from profanity_check import predict
from sklearn.externals import joblib


blocked_words = ["احا", "كلمة1", "كلمة2"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

mute_role_id = '1287139631418048543'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message) and "قوم بيهم" in message.content:
        await message.channel.send("حاضر من عيوني")

    for word in blocked_words:
        if word in message.content:
            await message.delete()
            mute_role = discord.utils.get(message.guild.roles, id=int(mute_role_id))
            if mute_role:
                await message.author.add_roles(mute_role)
            await message.channel.send(f"{message.author.mention} تم كتمك بسبب استخدام كلمات محظورة")
            return
    
    if predict([message.content])[0] == 1:
        await message.delete()
        await message.channel.send(f"{message.author.mention} تم كتمك بسبب استخدام كلمات محظورة")
        mute_role = discord.utils.get(message.guild.roles, id=int(mute_role_id))
        if mute_role:
            await message.author.add_roles(mute_role)
    
    await bot.process_commands(message)

bot.run("MTMwNTIyNTMxNzU0MzMxMzUzMw.G3FcIQ.lgH982KSbhzuOGfHBpLw46lCIapPkNTDPzmrBk")
