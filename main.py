from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import nextcord
import os
import random
from dotenv import load_dotenv

#get the bot token
load_dotenv() 

#things I have to set to make discord bots work
intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True
client = nextcord.Client(intents=intents)

tracks = [f"track_{i}" for i in range(1,3)]
data = pd.DataFrame({
    'user_id': [12345, 67890, 54321],
    'track_1': [120.5, 115.8, 122.4],
    'track_2': [118.2, 116.4, 123.1],
})

@client.event
async def on_ready():
    #get any existing data
    load_data() 

    #have bot hit TM API once every hour to reduce calls
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_times, 'interval', hours=1)
    scheduler.start() 

#grab the data from the CSV
def load_data():
    global data
    if os.path.exists("personal_bests.csv"):
        data = pd.read_csv("personal_bests.csv")

        #print column names to inspect
        print("Columns in CSV:", data.columns)

        #convert columns (except user_id) to numeric
        for track in tracks:
            if track in data.columns:
                data[track] = pd.to_numeric(data[track], errors='coerce')

        #check if user_id is in columns
        if 'user_id' not in data.columns:
            print("Error: 'user_id' column missing")
            return
        
        data.set_index('user_id', inplace=True)

        #print first few rows for inspection
        print(data.head())

    #if no data, create empty frame
    else:                       
        data = pd.DataFrame(columns=tracks)
        data.set_index('user_id', inplace=True)

#API call code goes here - for now, just generating random data for testing
def fetch_times(track):
    new_time = round(random.uniform(60.0, 120.0), 2)
    return new_time
    
#logic to detect new PB
def update_times():
    for user_id in data.index:
        if user_id not in data.index:
            data.loc[user_id] = {track: new_time}
        for track in tracks:
            new_time = fetch_times(track)
            update_pb(user_id, track, new_time)
            data.to_csv("personal_bests.csv", index=True)

#logic for checking if the data pulled from the API call is new, to update the CSV
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

#custom discord slash command for manually updating data
@client.slash_command(name='update', description='Update campaign times manually')
async def update(ctx, track: str):
    user_id = ctx.author.id
    new_time = fetch_times(track)
    update_pb(user_id, track, new_time)
    await ctx.send(f"{ctx.author.mention}, your new time for {track} is {new_time}")

#incase of bot closing, save the data
@client.event
async def on_close():
    data.reset_index(inplace=True)
    data.to_csv("Personal_bests.csv", index=False)

client.run(os.getenv('BOT_TOKEN'))