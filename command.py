# command interpreter
import discord
import confdb
import helper

from commands import cfgedit

async def interpret_command(message: discord.Message, conf_man: confdb.ConfManager):
    guild_conf = conf_man.get_db(message.guild.id)

    # incase you forgot the prefix
    if (message.content == "get_bettermee6_prefix"):
        await message.channel.send("The prefix is: " + str(guild_conf["prefix"]))

    if (not message.content.startswith(guild_conf["prefix"])):
        return
    
    base_command = message.content.removeprefix(guild_conf["prefix"])
    command_parts = base_command.split(" ")

    command_name = command_parts[0].lower()

    if (command_name == "hello"):
        await message.channel.send("Hello!")
    
    if (command_name == "set_maintenance_channel"):
        if (not message.author.guild_permissions.administrator):
            await helper.send_error("You cannot run this command", message)
            return
        guild_conf["maintenance_channel"] = message.channel.id
        conf_man.save_db(message.guild.id, guild_conf)
        await helper.send_embed("Set Maintenance Channel", "This channel was set as the maintenance channel. You can view bot logs and configure the bots from here!\nTo change the maintenance channel, run the command again in another channel", 0x0000ff, message)
    
    if (command_name == "cfgedit"):
        await cfgedit.run(guild_conf, command_parts, conf_man, message)