**Useful Links**

[ares-sc2 framework repo](https://github.com/AresSC2/ares-sc2)  
[ares-sc2 documentation](https://aressc2.github.io/ares-sc2/index.html)

---
# Installation

If you're looking to build your own StarCraft II bot, starting with the `ares-sc2-bot-template` let's you get up and running quickly. This template uses the  Ares-sc2 framework which builds upon the python-sc2 framework, enhancing its capabilities for bot development in StarCraft II. You can find it [here](https://aressc2.github.io/ares-sc2/index.html). 

### Prerequisites

Before proceeding, ensure the following prerequisites are installed:

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Poetry](https://python-poetry.org/) 
- [Git](https://git-scm.com/)
- [Starcraft 2](https://starcraft2.com/en-gb/) 
- [Maps](https://sc2ai.net/wiki/maps/) Ensure maps are moved to the correct folder as suggested in this wiki.


**Additional:**

*Linux:*  can either download the SC2 Linux package [here](https://github.com/Blizzard/s2client-proto#linux-packages)  from Blizzard or, alternatively, set up Battle.net via WINE using this [lutris script](https://lutris.net/games/battlenet/). 

 [PyCharm IDE](https://www.jetbrains.com/pycharm/) - This tutorial will demonstrate how to set up a bot development environment using PyCharm but you can use any IDE.

The maps must be copied into the **root** of the Starcraft 2 maps folder - default location: `C:\Program Files (x86)\StarCraft II\Maps`.
## Environment Setup for Linux (Lutris)

If you've installed StarCraft II using Lutris on Linux, you'll need to set some environment variables so that the `ares-sc2` library can correctly interact with the game.

### Setting Environment Variables Temporarily

Open a terminal and enter the following commands, replacing `(username)` with your actual Linux username and `(version of wine)` with the version of Wine that Lutris is using:

```shell
export SC2PF=WineLinux
export SC2PATH="/home/`(username)`/Games/battlenet/drive_c/Program Files (x86)/StarCraft II/"
export WINE="/home/`(username)`/.local/share/lutris/runners/wine/`(version of wine)`/bin/wine" 
```


# Creating Your Bot

- Visit the [starter-bot repo](https://github.com/AresSC2/ares-sc2-starter-bot) and click the `Use this template` button to create your own repository based on this template. The repository can be either public or private.
    
- Next, clone the repository locally to your system, ensuring you include the `--recursive` flag:
    
```bash
git clone --recursive <your_git_repo_home_url_here>
```

- Open a terminal or console window.
    
- Navigate to the root of your bot's directory:

```bash
cd <bot_folder>
```

- Install dependencies, compile Cython, and create a new isolated virtual environment:

```bash
poetry install
```

### Testing Your Bot:

If you have a non-standard StarCraft 2 installation or are using Linux, please adjust `MAPS_PATH` in `run.py`.

Optionally set your bot name and race in `config.yml`

```bash
poetry run python run.py
```

## Start Developing Your Bot

If everything has worked thus far, open up `bot/main.py` and delve into the excitement of bot development!

An `ares-sc2` bot is a [python-sc2](https://github.com/BurnySc2/python-sc2) bot by default, meaning any examples or documentation from that repository equally relevant here.

## Uploading to [AiArena](https://www.sc2ai.com/)

### Generating a ladder zip
Included in the repository is a convenient script named `scripts/create_ladder_zip.py`. 
However, it is important to note that the AIarena ladder infrastructure operates specifically 
on Linux-based systems. Due to the dependency of ares-sc2 on cython, it is necessary to execute 
this script on a Linux environment in order to generate Linux binaries.

To streamline this process, a GitHub workflow has been integrated into this repository when
pushing to `main` on your GitHub repository (if you previously created a template
from the [starter-bot](https://github.com/AresSC2/ares-sc2-starter-bot)). 
Upon each push to the main branch, the `create_ladder_zip.py` script is automatically
executed on a Debian-based system. As a result, a compressed artifact 
named `ladder-zip.zip` is generated, facilitating the subsequent upload to AIarena. 
To access the generated file, navigate to the Actions tab, click on an Action and refer to the 
Artifacts section. Please note this may take a few minutes after pusing to the `main` branch.

Ladder zips can also be built on a debian based OS, with docker or via WSL.

### Upload to aiarena
The GitHub workflow includes an optional step to automatically upload the ladder-zip.zip artifact from 
the previous step to the [AiArena ladder](https://www.sc2ai.com/). This feature is disabled by default. 
To enable it, follow these steps:

1. Set `AutoUploadToAiarena: True` in `config.yml`.
2. Visit the AiArena ladder and create an account if you don't have one.
3. If necessary, set up a new bot via the AiArena website.
4. Navigate to your bot's profile and note your bot ID, which can be found in the URL.
5. Go to `Profile -> View API Token` and save the token string.
6. In your bot's GitHub repository, navigate to `Settings -> Secrets and variables -> Actions`.
7. Create two new secrets with the following exact names, using the api token and bot id from earlier:

UPLOAD_API_TOKEN: <aiarena_api_token> <br />
UPLOAD_BOT_ID: <bot_id>

After completing these steps, the next push to the main branch will build the ladder zip artifact 
and automatically upload it to AiArena. You can customize this workflow as needed.

---
# Additional
## PyCharm

#### Adding `poetry` environment

Find the path of the environment `poetry` created in the installation step previously, copy and paste or save this path somewhere.

`poetry env list --full-path`

Open this project in PyCharm and navigate to:

File | Settings | Project: | Python Interpreter

- Click `Add Interpreter`, then `Add Local Interpreter`

![Alt text](https://aressc2.github.io/ares-sc2/tutorials/img/img1.png "a title")

- Select `Poetry Environment`, and choose `Existing Environment`
- Navigate to the path of the poetry environment from the terminal earlier, and select `Scripts/python.exe`

![Alt text](https://aressc2.github.io/ares-sc2/tutorials/img/img2.png "a title")

Now when opening terminal in PyCharm, the environment will already be active. New run configurations can be setup, and they will already be configured to use this environment.

#### Marking sources root

For PyCharm intellisense to work correctly: - Right-click `ares-sc2/src` -> Mark Directory as -> Sources Root

![Alt text](https://aressc2.github.io/ares-sc2/tutorials/img/img3.png "a title")

## Installing Poetry on Linux

To get Poetry to run on some Linux distros you may need to perform the following

```bash
python3 --version
```
to check your version of python, it should show 3.10.12 then 

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
to install poetry

```bash
poetry --version
```
to verify you have poetry installed

## Update `ares-sc2`

This may take a minute or two

`python scripts/update_ares.py`

## Format code

`black .`

`isort .`

# FAQ

I got the Following Error `Directory .../ares-sc2-bot-template/ares-sc2 for ares-sc2 does not seem to be a Python package`

a: This means you're missing the ares-sc2 sub module 
```bash
git submodule update --init
git submodule update --init --recursive --remote
```

--- 
***Interested in contributing*** to `ares-sc2`? Take a look at setting up a local dev environment [here instead.](https://aressc2.github.io/ares-sc2/contributing/index.html)
