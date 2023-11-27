import discord
from discord.ext import commands
import random
import time

TOKEN = "MTE3ODQ3MjAyMzE1NzEyNTI2MQ.GwQbqD.AyrsG2n91emPfH9mIpi0cE5PI-cIScScOqpra8"
PREFIX = "$"
ROLE_ID_TO_ASSIGN = 1178488708001959988  # Replace with your desired role ID

intents = discord.Intents.default()
intents.message_content = True  # Enable message content in the on_message event

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
active_keys = {}  # Dictionary to store active keys and their expiration times

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='keygen')
async def generate_key(ctx, time_limit: int = 1):
    key = generate_random_key()
    expiration_time = time.time() + (time_limit * 24 * 60 * 60)  # Convert days to seconds

    active_keys[key] = expiration_time

    with open('keysActive.txt', 'a') as file:
        file.write(f"{key} {expiration_time}\n")

    await ctx.send(f"Key generated: {key} (Expires in {time_limit} days)")

@bot.command(name='key_claim')
async def claim_key(ctx, key: str):
    if key in active_keys and time.time() < active_keys[key]:
        del active_keys[key]
        user = ctx.message.author
        role = ctx.guild.get_role(ROLE_ID_TO_ASSIGN)
        await user.add_roles(role)
        await ctx.send(embed=discord.Embed(description="Success, Key Activated! Role Assigned.", color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(description="Invalid or expired key.", color=discord.Color.red()))

@bot.command(name='key_abort')
async def abort_key(ctx, key: str):
    if key in active_keys:
        del active_keys[key]
        await ctx.send(embed=discord.Embed(description="Key aborted and invalidated.", color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(description="Invalid key.", color=discord.Color.red()))

@bot.command(name='key_rev')
async def revive_key(ctx, key: str):
    # Check if the key was previously aborted
    if key not in active_keys:
        active_keys[key] = time.time()  # Revive the key with no expiration time
        await ctx.send(embed=discord.Embed(description="Key revived and set to active.", color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(description="Key is already active.", color=discord.Color.red()))

def generate_random_key():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

bot.run(TOKEN)
