# cfgedit command (example uses default prefix)
#   ;cfgedit view <KEY>         # Views config data for KEY
#   ;cfgedit set <KEY> <VAL>         # Sets config data for KEY (key must already exist)
# Must be run in a maintenance channel by an admin

import discord
import sys
sys.path.append("..")

import helper
import confdb

async def _set(guild_conf, key, val, conf_man: confdb.ConfManager, message: discord.Message):
    if key not in guild_conf:
        await helper.send_error("The key ``" + str(key) + "`` doesn't exist in the configuration file", message)
        return
    guild_conf[key] = val
    conf_man.save_db(message.guild.id, guild_conf)
    await helper.send_embed("ConfigEdit Set", "Key: ``" + str(key) + "`` = Value: ``" + str(val) + "``", 0x00ff00, message)

async def _view(guild_conf, key, message: discord.Message):
    if key not in guild_conf:
        await helper.send_error("The key ``" + str(key) + "`` doesn't exist in the configuration file", message)
        return
    await helper.send_embed("ConfigEdit View", "Key: ``" + str(key) + "`` = Value: ``" + str(guild_conf[key]) + "``", 0x00ff00, message)

async def run(guild_conf, command_parts, conf_manager: confdb.ConfManager, message: discord.Message):
    if (not message.author.guild_permissions.administrator):
        await helper.send_error("You cannot run this command", message)
        return
    
    if (message.channel.id != guild_conf["maintenance_channel"]):
        await helper.send_error("Command must be run in a maintenance channel.", message)
        return

    if (len(command_parts) < 3):
        await helper.send_error("Invalid number of arguments provided\n``" + str(guild_conf["prefix"]) + "cfgedit view <KEY>`` or ``"  + str(guild_conf["prefix"]) + "cfgedit set <KEY> <VAL>``", message)
        return
    
    if (command_parts[1] != 'set' and command_parts[1] != 'view'):
        await helper.send_error("Unknown action '" + command_parts[1] + "', this command only supports: 'set' and 'view'", message)
        return
    
    if (command_parts[1] == "set"):
        if (len(command_parts) != 4):
            await helper.send_error("Invalid number of arguments provided\n``"  + str(guild_conf["prefix"]) + "cfgedit set <KEY> <VAL>``", message)
            return
        await _set(guild_conf, command_parts[2], command_parts[3], conf_manager, message)
    elif (command_parts[1] == "view"):
        if (len(command_parts) != 3):
            await helper.send_error("Invalid number of arguments provided\n``"  + str(guild_conf["prefix"]) + "cfgedit view <KEY>``", message)
            return
        await _view(guild_conf, command_parts[2], message)