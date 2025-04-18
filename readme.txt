Discord bot that checks the current TM2020 season leaderboard for clan members PBs and notifies when new records are set.

TO DO:
-Fix the logic for updating the .CSV (the test envi is not updating any data)
-Make logic for notifying of new times after the hourly check
-Actually make the logic for doing things once an hour
-Figure out how to remove the index.js and ids.py files without git bash throwing a tantrum
-Link ubisoft IDs to discord IDs (maybe with a way for users to set with a slash command)
-Figure out Heroku scheduling so the bot isn't constantly running and eating up dyno hours
-Make sure I didn't wreck things by getting pandas working
-Other things I can't remember