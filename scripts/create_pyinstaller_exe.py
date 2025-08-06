
import shutil
import subprocess
from os import path, remove
import platform
import site
import yaml
import glob
import json
import sys

# Check for Windows
if not platform.system() == 'Windows':
    print("Error: This script is intended to run only on Windows.")
    sys.exit(1)

FILE_NAME: str = "aresbot"
MY_BOT_NAME: str = "MyBotName"  # Changed to match config.yml key
MY_BOT_RACE: str = "MyBotRace"  # Added to match config.yml key
CONFIG_FILE: str = "config.yml"
BUILD_FILES = [
    'zerg_builds.yml', 'zerg_builds.yaml',
    'protoss_builds.yml', 'protoss_builds.yaml',
    'terran_builds.yml', 'terran_builds.yaml'
]

class PyInstaller:
    def __init__(self):
        self.project_root = path.dirname(path.dirname(path.abspath(__file__)))

        # Get the site-packages directory
        site_packages = site.getsitepackages()[0]

        self.pyinstaller = [
            "pyinstaller",
            "-y",
            "--onefile",
            "--add-data", f"{self.project_root}/config.yml;.",
            "--add-data", f"{self.project_root}/ares-sc2/src/ares;ares/",
            "--add-data", f"{self.project_root}/bot;bot/",
            "--add-data", f"{self.project_root}/ares-sc2/sc2_helper;sc2_helper/",
            f"{self.project_root}/run.py",
            "-n", FILE_NAME,
            "--distpath", path.join(self.project_root, "publish"),
            "--collect-all", "sc2",
            "--collect-all", "cython_extensions",
            "--collect-all", "scipy",
            "--collect-all", "numpy",
            "--collect-all", "map_analyzer",
            "--hidden-import", "sc2.paths",
            "--hidden-import", "cython_extensions",
            "--hidden-import", "scipy.signal",
            "--hidden-import", "scipy",
            "--hidden-import", "map_analyzer",
            "--hidden-import", "sc2_helper",
            "--hidden-import", "sc2_helper.combat_simulator",
            "--paths", site_packages,
            "--paths", f"{self.project_root}/ares-sc2/src",
        ]

    def get_config_values(self) -> tuple[str, str]:
        """Get bot name and race from config."""
        user_config_path: str = path.join(self.project_root, CONFIG_FILE)
        bot_name = FILE_NAME
        bot_race = "Random"  # Default value

        if path.isfile(user_config_path):
            with open(user_config_path) as config_file:
                config: dict = yaml.safe_load(config_file)
                if MY_BOT_NAME in config:
                    bot_name = config[MY_BOT_NAME]
                if MY_BOT_RACE in config:
                    bot_race = config[MY_BOT_RACE]

        return bot_name, bot_race

    def create_ladderbots_json(self, output_dir: str):
        """Create the ladderbots.json file."""
        bot_name, bot_race = self.get_config_values()
        exe_name = f"{bot_name}.exe"

        ladderbots_data = {
            "Bots": {
                bot_name: {
                    "Race": bot_race,
                    "Type": "BinaryCpp",
                    "RootPath": "./",
                    "FileName": exe_name,
                    "Args": "-O",
                    "Debug": True
                }
            }
        }

        ladderbots_path = path.join(output_dir, "ladderbots.json")
        with open(ladderbots_path, 'w') as f:
            json.dump(ladderbots_data, f, indent=2)
        print(f"Created ladderbots.json at {ladderbots_path}")

    def copy_build_files(self, output_dir: str):
        """Copy build files to the executable directory."""
        print("Copying build files...")
        for build_file in BUILD_FILES:
            # Search for the file in the project root and its subdirectories
            matches = glob.glob(path.join(self.project_root, '**', build_file), recursive=True)
            for match in matches:
                try:
                    shutil.copy2(match, output_dir)
                    print(f"Copied {match} to {output_dir}")
                except Exception as e:
                    print(f"Failed to copy {match}: {e}")

    def package_executable(self):
        print("Running PyInstaller...")
        output_dir = path.join(self.project_root, "publish")

        # Set the name in the pyinstaller command
        name = self.get_config_values()[0]  # Get bot name from config
        self.pyinstaller[self.pyinstaller.index("-n") + 1] = name

        # Print the command for debugging
        print("Running command:", " ".join(self.pyinstaller))
        process = subprocess.run(self.pyinstaller, check=True)

        if process.returncode == 0:
            print("PyInstaller completed successfully")
            self.copy_build_files(output_dir)
            self.create_ladderbots_json(output_dir)
        else:
            print("PyInstaller failed")


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