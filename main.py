import discord
from discord.ext import commands
from keep_alive import keep_alive
import json
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)

log_channel_id = 1267537601624145961

def load_invites():
    try:
        with open("invites.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_invites(invites_data):
    with open("invites.json", "w") as file:
        json.dump(invites_data, file)

@bot.event
async def on_member_join(member):
    invites = await member.guild.invites()
    invites_data = load_invites()

    for invite in invites:
        if invite.uses > invites_data.get(str(invite.code), {}).get("uses", 0):
            invites_data[str(invite.code)] = {
                "uses": invite.uses,
                "inviter": invite.inviter
            }

            log_channel = member.guild.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(f"{member.mention} joined using invite code {invite.code}. Invited by: {invite.inviter.mention}")

            break

    save_invites(invites_data)
    print(f"{member.name} joined using invite code {invite.code} by {invite.inviter.name}")

@bot.command()
async def invites(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    invites = await ctx.guild.invites()
    invites_data = load_invites()
    total_invites = 0
    inviter = None

    for invite in invites:
        if str(invite.code) in invites_data:
            total_invites += invite.uses - invites_data[str(invite.code)]["uses"]
            inviter = invites_data[str(invite.code)]["inviter"]

    if inviter:
        await ctx.send(f"{member.name} has invited {total_invites} members. Last invite was by {inviter.mention}.")
    else:
        await ctx.send(f"{member.name} has not invited anyone.")

@bot.command()
async def who_invited(ctx, invite_code: str):
    invites_data = load_invites()

    if invite_code in invites_data:
        inviter_name = invites_data[invite_code]["inviter"]
        await ctx.send(f"The invite code {invite_code} was created by {inviter_name.mention}.")
    else:
        await ctx.send(f"No data found for invite code {invite_code}.")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))