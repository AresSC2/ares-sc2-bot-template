# ares-sc2-starter-bot

[Documentation](https://aressc2.github.io/ares-sc2/index.html)

## Installation:
Prerequisites, ensure these are installed before proceeding:
- Python 3.9+ 
- [Poetry](https://python-poetry.org/)
- [Git](https://git-scm.com/)
- [Starcraft 2](https://starcraft2.com/en-gb/)
- [Maps](https://sc2ai.net/wiki/maps/)

### Windows
If you have a non-standard starcraft installation, please adjust `MAPS_PATH` in `run.py`

Clone, don't forget `--recursive`:

`git clone --recursive https://github.com/AresSC2/ares-sc2-starter-bot.git`

Install - this will install dependencies and create a new isolated virtual environment:

`poetry install`

Compile cython code:

`cd ares-sc2`

`python build.py build_ext --inplace`

Go back to root directory

`cd ..`

Run:

`poetry run python run.py`

### Linux
Not currently tested but steps above should be similar. `MAPS_PATH` in `run.py` will need to be changed

### PyCharm

#### Adding `poetry` environment
Find the path of the environment `poetry` created in the installation step previously, copy and paste
or save this path somewhere.

`poetry env list --full-path`


Open this project in PyCharm and navigate to:

File | Settings | Project: <project name> | Python Interpreter

 - Click `Add Interpreter`, then `Add Local Interpreter`

![Alt text](img/img1.png "a title")

 - Select `Poetry Environment`, and choose `Existing Environment`
 - Navigate to the path of the poetry environment from the terminal earlier, and select `Scripts/python.exe`

![Alt text](img/img2.png "a title")

Now when opening terminal in PyCharm, the environment will already be active. New run configurations can be setup,
and they will already be configured to use this environment.


#### Marking sources root
For PyCharm intellisense to work correctly:
 - Right-click `ares-sc2/src` -> Mark Directory as -> Sources Root
![Alt text](img/img3.png "a title")

   
## Update `ares-sc2`:
### Revert local changes to ares-sc2

`git submodule deinit -f .`

`git submodule update --init`

### Update

`git submodule update --init --recursive --remote`

`cd ares-sc2`

`python build.py build_ext --inplace`

## Format code:
`black .`
