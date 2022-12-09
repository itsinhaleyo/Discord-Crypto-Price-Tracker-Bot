import json
import os
import platform
import random
import sys
import re
import requests
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = disnake.Intents.default()
intents.messages = True
prefix = disnake.ext.commands.when_mentioned
bot = Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    status_task.start()

@tasks.loop(minutes=0.1)
async def status_task() -> None:
    data = requests.get("https://flarecasino.ca/fcprice.json").json()
    if data["price"]["percent_change_12h"] >= 0:
        status2 = ["$"+data["price"]["price"]+"📈"+data["price"]["percent_change_12h"]+"%"]
        await bot.change_presence(activity=disnake.Game(random.choice(status2)))
    else:
        status2 = ["$"+data["price"]["price"]+"📉"+data["price"]["percent_change_12h"]+"%"]
        await bot.change_presence(activity=disnake.Game(random.choice(status2)))

bot.run(os.environ["DISCORD_TOKEN"])
