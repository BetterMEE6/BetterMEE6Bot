import discord

async def send_embed(title, desc, colour, message: discord.Message):
    embed = discord.Embed(title=title, description=desc, color=colour)
    await message.channel.send(embed=embed)

async def send_error(err_msg, message: discord.Message):
    await send_embed("Error", err_msg, 0xff0000, message)
