#This program is meant for identifying duplicates in the leaderboard.json file
import json

list = []

with open('leaderboard.json', 'r+') as f:
    leaderboardFile = json.load(f)

for key in leaderboardFile:
    if key in list == True:
        print(f'{key}, is a duplicate')
    else:
        list.append(key)
