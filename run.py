import random
import sys
from pathlib import Path
from typing import List

from sc2 import maps
from sc2.data import AIBuild, Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer

sys.path.append("ares-sc2/src/ares")
sys.path.append("ares-sc2/src")
sys.path.append("ares-sc2")

from bot.main import MyBot

from ladder import run_ladder_game

MAP_FILE_EXT: str = "SC2Map"
# change if non default setup
MAPS_PATH: str = "C:\\Program Files (x86)\\StarCraft II\\Maps"

bot1 = Bot(Race.Random, MyBot(), "MyBot")


def main():
    # Ladder game started by LadderManager
    print("Starting ladder game...")
    result, opponentid = run_ladder_game(bot1)
    print(result, " against opponent ", opponentid)


# Start game
if __name__ == "__main__":
    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(bot1)
        print(result, " against opponent ", opponentid)
    else:
        # Local game
        map_list: List[str] = [
            p.name.replace(f".{MAP_FILE_EXT}", "")
            for p in Path(MAPS_PATH).glob(f"*.{MAP_FILE_EXT}")
            if p.is_file()
        ]

        random_race = random.choice([Race.Zerg, Race.Terran, Race.Protoss])
        print("Starting local game...")
        run_game(
            maps.get(random.choice(map_list)),
            [
                bot1,
                Computer(random_race, Difficulty.CheatVision, ai_build=AIBuild.Macro),
            ],
            realtime=False,
        )
