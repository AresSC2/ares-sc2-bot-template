import shutil
import subprocess
from os import path, remove
import platform

import yaml

FILE_NAME: str = "aresbot"
MY_BOT_NAME: str = "AresBot"
CONFIG_FILE: str = "config.yml"


class PyInstaller:
    def __init__(self):
        # Break down the command into a list of arguments
        self.pyinstaller = [
            "pyinstaller",
            "-y",
            "--onefile",
            "--add-data", "[FOLDER]/ares-sc2:ares-sc2/",
            "--add-data", "[FOLDER]/bot:bot/",
            "[FOLDER]/run.py",
            "-n", "[NAME]",
            "--distpath", "[OUTPUTFOLDER]"
        ]
        # Handle Windows path separator differently
        if platform.system() == "Windows":
            # Use semicolon for Windows
            self.pyinstaller[4] = "[FOLDER]/ares-sc2;ares-sc2/"
            self.pyinstaller[6] = "[FOLDER]/bot;bot/"

    def get_file_name(self) -> str:
        """Attempt to get bot name from config."""
        __user_config_location__: str = path.abspath(".")
        user_config_path: str = path.join(__user_config_location__, CONFIG_FILE)
        file_name = FILE_NAME
        # attempt to get race and bot name from config file if they exist
        if path.isfile(user_config_path):
            with open(user_config_path) as config_file:
                config: dict = yaml.safe_load(config_file)
                if MY_BOT_NAME in config:
                    file_name = f"{config[MY_BOT_NAME]}"
        return file_name

    def package_executable(self):
        print("Running PyInstaller...")
        # Replace placeholders in the command list
        command = [
            arg.replace("[FOLDER]", "../")
            .replace("[OUTPUTFOLDER]", "../publish")
            .replace("[NAME]", f"{self.get_file_name()}")
            for arg in self.pyinstaller
        ]

        # Run PyInstaller with the formatted command
        subprocess.run(command, check=True)


if __name__ == "__main__":
    # Remove old build cache if it exists
    path_to_build_cache = path.join(".", "build")
    if path.exists(path_to_build_cache):
        shutil.rmtree(path_to_build_cache)

    # Also remove any existing spec file
    spec_file = path.join(".", "ares.spec")
    if path.exists(spec_file):
        remove(spec_file)

    pyins = PyInstaller()
    pyins.package_executable()