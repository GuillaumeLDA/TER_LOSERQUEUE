"""
This script gets the match IDs for each summoner obtained.
"""

#Lib
import requests
import time
import json
import pandas as pd

num = 100  #Numnber 

#API Key
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/apiKey.txt", 'r') as file:
    apiKey = file.read().strip()

#Puuid file
puuid_name_map = {}
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/summoners_info.json", 'r') as file:
    data = json.load(file)
    for entry in data:
        puuid_name_map[entry['id']] = entry['puuid']


match_ids_data = []
i = 1
total_requests = len(puuid_name_map) 
match_history_details = []


for idx, (id, puuid) in enumerate(puuid_name_map.items(), start=1):
    prct = i / total_requests
    print('Progress : ', (round(prct*100,2)), "%")
    response = requests.get(
        f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime=1704888000&type=ranked&start=0&count={num}&api_key={apiKey}')
    if response.status_code == 200:
        match_ids = response.json()
        for match_id in match_ids:
            match_ids_data.append(match_id)
        match_history_details.append(f"{puuid} ({id}): {len(match_ids)} matchs")
    else:
        print(f"Failure for {id} (puuid: {puuid}), Code: {response.status_code}")
    i += 1
    time.sleep(1.3)


with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Match_ID.txt', 'a') as f_match_id:
    for match_id in match_ids_data:
        f_match_id.write(match_id + '\n')


with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/details_match_history.txt', 'w') as f_details:
    for detail in match_history_details:
        f_details.write(detail + '\n')