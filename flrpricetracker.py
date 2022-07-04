import json
import os
import platform
import random
import sys
import re

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

import exceptions

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
    flrprice = cg.get_price(ids='flare-token', vs_currencies='usd', include_24hr_change='true')
    price = re.findall("\d+", str(flrprice))[1]
    price2 = re.findall("\d+", str(flrprice))[0]
    price3 = re.findall("\d+", str(flrprice))[3]
    price4 = re.findall("\d+", str(flrprice))[4]
    run = str(re.sub(r'[^-]', "", str(flrprice)))
    flr = len(run)
    if flr == 2:
        status1 = ["$"+str(price2)+"."+str(price[:7])+"📉"+str(price3)+"."+str(price4[:2])+"%"]
        await bot.change_presence(activity=disnake.Game(random.choice(status1)))
    elif flr == 1:
        status2 = ["$"+str(price2)+"."+str(price[:7])+"📈"+str(price3)+"."+str(price4[:2])+"%"]
        await bot.change_presence(activity=disnake.Game(random.choice(status2)))

bot.run(config["token"])
