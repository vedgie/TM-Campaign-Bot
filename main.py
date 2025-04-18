# import all the bot shit first

# sleep 30 seconds
# TRY:
#   Check channels
#   if conditions met:
#       Do the reactions
#       wait x time
#       if x time with no reactions
#           sleep 30 seconds
# EXCEPT:
#   sleep 30 seconds

from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import nextcord
from nextcord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv


intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True
client = nextcord.Client(intents=intents)
tracks = [f"track_{i}" for i in range(1,26)]
data = None

@client.event
async def on_ready():
    load_data()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_times, 'interval', hours=1)
    scheduler.start()

def update_times():
    for user_id in data.index:
        for track in tracks:
            new_time = fetch_times
            update_pb(user_id, track, new_time)
    data.to_csv("personal_bests.csv")

def load_data():
    global data
    if os.path.exists("personal_bests.csv"):
        data = pd.read_csv("personal_bests.csv", index_col="user_id")
    else:                       
        data = pd.DataFrame(columns=tracks)
        data.set_index('user_id', inplace=True)

def fetch_times(track):
    return round(random.uniform(60.0, 120.0), 2)

def update_pb(user_id, track, new_time):
    global data

    if user_id not in data.index:
        data.loc[user_id] = {track: new_time}
        return

    if track not in data.columns:
        return
    
    current_best = data.at[user_id, track]

    if pd.isna(current_best) or new_time < current_best:
        data.at[user_id, track] = new_time

@client.slash_command(name='Update', description='Update campaign times manually')
async def race(ctx, track: str):
    user_id = ctx.author.id
    new_time = fetch_times(track)
    update_pb(user_id, track, new_time)
    await ctx.send(f"{ctx.author.mention}, your new time for {track} is {new_time}")

@client.event
async def on_close():
    data.to_csv("Personal_bests.csv")

client.run(os.getenv('BOT_TOKEN'))