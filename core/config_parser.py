import configparser
import os


class ConfigParser:
    def __init__(self):
        setting_path = os.path.dirname(os.path.abspath(__file__)) + "./../settings.ini"
        self.ui_info_path = (
            os.path.dirname(os.path.abspath(__file__)) + "../../WindowsInfo.ini"
        )

        Config = configparser.ConfigParser()
        Config.read(setting_path)
        self.window_name = Config.get("Settings", "WindowName")
        self.is_debug = Config.get("Settings", "Debug")
        self.player_class = Config.get("Settings", "Class")
        self.abilities = Config.get("Settings", "Abilities").split(",")
