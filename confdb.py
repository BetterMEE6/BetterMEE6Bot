# db manager for all guilds

import os
import json
import time

default_values = {
    "prefix": ';',
    "maintenance_channel": -1,

    "welcomer": False,
    "welcomer_message": "Hey! Welcome to the server. We don't use MEE6!"
}

db_dir = "guild_conf/"

class ConfManager():
    def __init__(self) -> None:
        self.conf_cache = [{"expires":0, "gid": 0, "conf":{}}]

    def __add_cached_conf(self, guild_id):
        if (os.path.exists(os.path.join(db_dir, str(guild_id) + ".conf"))):
            f = open(os.path.join(db_dir, str(guild_id) + ".conf"), "r")
            json_string = f.read()
            f.close()
            current_guild_dict = json.loads(json_string)

            self.conf_cache.append({"expires": (time.time() + 3600), "gid": guild_id, "conf": current_guild_dict})
            return current_guild_dict

        else:
            self.init_db(guild_id)
            return default_values

    def get_db(self, guild_id):
        for cached in self.conf_cache:
            if (cached["gid"] == guild_id):
                if cached["expires"] > time.time():
                    return cached["conf"]
                else:
                    del cached
        return self.__add_cached_conf(guild_id)

    def __edit_cache(self, guild_id, guild_conf):
        for cached in self.conf_cache:
            if (cached["gid"] == guild_id):
                if cached["expires"] > time.time():
                    cached["conf"] = guild_conf
                else:
                    del cached
        self.__add_cached_conf(guild_id)

    def save_db(self, guild_id, guild_conf):
        f = open(os.path.join(db_dir, str(guild_id) + ".conf"), "w")
        f.write(json.dumps(guild_conf))
        f.close()
        self.__edit_cache(guild_id, guild_conf)

    def init_db(self, guild_id):
        if (not os.path.exists(db_dir)):
            print("FATAL: cannot find guild_conf directory")
            return
        
        if (not os.path.exists(os.path.join(db_dir, str(guild_id) + ".conf"))):
            print(f"[{guild_id}] Creating New Guild Conf")
            f = open(os.path.join(db_dir, str(guild_id) + ".conf"), "w")
            f.write(json.dumps(default_values))
            f.close()
        else:
            print(f"[{guild_id}] Checking Guild Conf...")
            
            f = open(os.path.join(db_dir, str(guild_id) + ".conf"), "r")
            json_string = f.read()
            f.close()

            current_guild_dict = json.loads(json_string)
            vals_added = 0

            for conf in default_values:
                if conf not in current_guild_dict:
                    current_guild_dict[conf] = default_values[conf]
                    vals_added += 1
            
            print(f"[{guild_id}] added {str(vals_added)} value(s)")
            
            if vals_added > 0:
                f = open(os.path.join(db_dir, str(guild_id) + ".conf"), "w")
                f.write(json.dumps(current_guild_dict))
                f.close()