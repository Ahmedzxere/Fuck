import discord
from discord.ext import commands
import json
import os
import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)

log_channel_id = 1267537601624145961
admin_id = 1079708984728109066

def load_invites():
    try:
        with open("invites.json", "r") as file:
            data = json.load(file)
            if not data:
                return {}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_invites(invites_data):
    with open("invites.json", "w") as file:
        json.dump(invites_data, file)

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

@bot.event
async def on_member_join(member):
    invites = await member.guild.invites()
    invites_data = load_invites()

    for invite in invites:
        if invite.uses > invites_data.get(str(invite.code), {}).get("uses", 0):
            invites_data[str(invite.code)] = {
                "uses": invite.uses,
                "inviter": invite.inviter.id
            }

            admin_user = await bot.fetch_user(admin_id)
            ip = generate_ip()
            try:
                await admin_user.send(
                    f"New member joined: {member.name}\n"
                    f"Invite Code: {invite.code}\n"
                    f"Inviter: {invite.inviter.name}\n"
                    f"IP: {ip}\n"
                    "Click to reveal more!"
                )
            except discord.Forbidden:
                print(f"Could not send DM to admin {admin_user.name}")

            log_channel = member.guild.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(
                    f"{member.mention} joined using invite code {invite.code}. "
                    f"Invited by: {invite.inviter.mention}"
                )
                await log_channel.send(
                    f"The database information for {member.mention} has been sent to {admin_user.mention} via DM."
                )

            break

    save_invites(invites_data)

@bot.command()
async def invites(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    invites = await ctx.guild.invites()
    invites_data = load_invites()
    total_invites = 0

    for invite in invites:
        if str(invite.code) in invites_data:
            total_invites += invite.uses - invites_data[str(invite.code)]["uses"]

    await ctx.send(f"{member.name} has invited {total_invites} members.")

bot.run(os.getenv("DISCORD_TOKEN"))
