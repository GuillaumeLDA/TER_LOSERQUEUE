"""
Getting data for the 2nd part of the project. 
The Objective is to get the match history of a specific player. 
The Riot API limits extraction to 100 match IDs at a time for a player, 
so we first calculate time intervals in Unix timestamp format (the format that Riot uses). 
This allows us to divide our searches into monthly increments since RIOT started storing match IDs (in June 2021).
"""

#lib
import requests
import time
import json
import pandas as pd
import datetime
import calendar

#Get time
def to_unix_timestamp(year, month, day):
    return int(datetime.datetime(year, month, day).timestamp())

start_date = datetime.datetime(2021, 7, 1)
end_date = datetime.datetime(2024, 5, 25)
start = []
end = []
current_date = start_date
while current_date < end_date:
    start_timestamp = to_unix_timestamp(current_date.year, current_date.month, 1)
    start.append(start_timestamp)

    last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
    end_timestamp = to_unix_timestamp(current_date.year, current_date.month, last_day_of_month)
    end.append(end_timestamp)

    if current_date.month == 12:
        current_date = datetime.datetime(current_date.year + 1, 1, 1)
    else:
        current_date = datetime.datetime(current_date.year, current_date.month + 1, 1)

num = 100 
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/apiKey.txt", 'r') as file:
    apiKey = file.read().strip()

puuid_name_map = {}
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/summoners_info_kr.json", 'r') as file:
    data = json.load(file)
    for entry in data:
        puuid_name_map[entry['id']] = entry['puuid']

match_ids_data = []
i = 1
total_requests = len(puuid_name_map)  
match_history_details = []
for j in range(0, len(start)):
    date_string = datetime.datetime.fromtimestamp(start[j]).strftime('%Y-%m-%d %H:%M:%S')
    print('Date : ', date_string)
    for idx, (id, puuid) in enumerate(puuid_name_map.items(), start=1):
        prct = i / total_requests
        print('Progress : ', (round(prct*100,2)), "%")
        response = requests.get(
            f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start[j]}&endTime={end[j]}&type=ranked&start=0&count={num}&api_key={apiKey}')
        if response.status_code == 200:
            match_ids = response.json()
            for match_id in match_ids:
                match_ids_data.append(match_id)
            match_history_details.append(f"{puuid} ({id}): {len(match_ids)} matchs")
        else:
            print(f"Failure for {id} (puuid: {puuid}), Code: {response.status_code}")
        i += 1
        time.sleep(1.3)


with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Match_ID_kr.txt', 'a') as f_match_id:
    for match_id in match_ids_data:
        f_match_id.write(match_id + '\n')

# Écriture des détails dans le fichier details_match_history.txt
with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/details_match_history_kr.txt', 'w') as f_details:
    for detail in match_history_details:
        f_details.write(detail + '\n')

# Lire les matchs
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Match_ID_kr.txt", 'r') as f:
    matches = f.read().splitlines()

with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/summoners_info_kr.json", 'r') as file:
    summoners_data = json.load(file)
    summoner_puuids = [summoner['puuid'] for summoner in summoners_data]

def process_match(match_id):
    response = requests.get(f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={apiKey}')
    if response.status_code == 200:
        match_data = response.json()
        metadata = match_data['metadata']
        info = match_data['info']
        

        # Extraction des données
        match_id = metadata['matchId']
        participants_puuids = metadata['participants']
        GameTime = info['gameDuration'] / 60  # Convertir en minutes
        game_version_major = info['gameVersion'].split('.')[0]

        # Filtrer et extraire les données des participants sous forme de dictionnaire
        participant_data = []
        for participant in info['participants']:
            if participant['puuid'] in summoner_puuids:
                team = "Blue" if participants_puuids.index(participant['puuid']) + 1 <= 5 else "Red"
                resultwin = "Win" if participant['win'] == True else "Lose"
                participant_data.append({
                    'Match_ID': match_id,
                    'GameVersion': game_version_major,
                    'puuid' : participant['puuid'],
                    'Team': team, 
                    'GameTime': GameTime, 
                    'result': resultwin,
                    'individualPosition' : participant['individualPosition'],
                    'championName' : participant['championName'],
                    'kda' : participant['challenges'].get('kda'),
                    'kills' : participant['kills'],
                    'deaths' : participant['deaths'],
                    'assists' : participant['assists'],
                    'SoloKills' : participant['challenges'].get('soloKills'),
                    'quickSoloKills' : participant['challenges'].get('quickSoloKills'),
                    'killsUnderOwnTurret' : participant['challenges'].get('killsUnderOwnTurret'),
                    'killsNearEnemyTurret' : participant['challenges'].get('killsNearEnemyTurret'),
                    'firstBloodAssist' : participant['firstBloodAssist'],
                    'firstBloodKill' : participant['firstBloodKill'],
                    'doubleKills' : participant['doubleKills'],
                    'tripleKills' : participant['tripleKills'],
                    'quadraKills' : participant['quadraKills'],
                    'pentaKills' : participant['pentaKills'],
                    'killingSprees' : participant['killingSprees'],
                    'turretKills' : participant['turretKills'],
                    'quickFirstTurret' : participant['challenges'].get('quickFirstTurret'),
                    'firstTowerAssist' : participant['firstTowerAssist'],
                    'firstTowerKill' : participant['firstTowerKill'],
                    'turretPlatesTaken' : participant['challenges'].get('turretPlatesTaken'),
                    'kTurretsDestroyedBeforePlatesFall' : participant['challenges'].get('kTurretsDestroyedBeforePlatesFall'),
                    'champLevel' : participant['champLevel'],
                    'visionScore' : participant['visionScore'],
                    'visionScoreAdvantageLaneOpponent' : participant['challenges'].get('visionScoreAdvantageLaneOpponent'),
                    'visionScorePerMinute' : participant['challenges'].get('visionScorePerMinute'),
                    'totalMinionsKilled' : participant['totalMinionsKilled'],
                    'laneMinionsFirst10Minutes' : participant['challenges'].get('laneMinionsFirst10Minutes'),
                    'neutralMinionsKilled' : participant['neutralMinionsKilled'],
                    'skillshotsDodged' : participant['challenges'].get('skillshotsDodged'),
                    'skillshotsHit' : participant['challenges'].get('skillshotsHit'),
                    'dodgeSkillShotsSmallWindow' : participant['challenges'].get('dodgeSkillShotsSmallWindow'),
                    'goldPerMinute' : participant['challenges'].get('goldPerMinute'),
                    'goldEarned' : participant['goldEarned'],
                    'goldSpent' : participant['goldSpent'],
                    'laningPhaseGoldExpAdvantage' : participant['challenges'].get('laningPhaseGoldExpAdvantage'),
                    'damagePerMinute' : participant['challenges'].get('damagePerMinute'),
                    'magicDamageDealt' : participant['magicDamageDealt'],
                    'magicDamageDealtToChampions' : participant['magicDamageDealtToChampions'],
                    'magicDamageTaken' : participant['magicDamageTaken'],
                    'physicalDamageDealt' : participant['physicalDamageDealt'],
                    'physicalDamageDealtToChampions' : participant['physicalDamageDealtToChampions'],
                    'physicalDamageTaken' : participant['physicalDamageTaken'],
                    'trueDamageDealt' : participant['trueDamageDealt'],
                    'trueDamageDealtToChampions' : participant['trueDamageDealtToChampions'],
                    'trueDamageTaken' : participant['trueDamageTaken'],
                    'totalDamageDealt' : participant['totalDamageDealt'],
                    'totalDamageDealtToChampions' : participant['totalDamageDealtToChampions'],
                    'totalDamageTaken' : participant['totalDamageTaken'],
                    'damageDealtToBuildings' : participant['damageDealtToBuildings'],
                    'damageDealtToObjectives' : participant['damageDealtToObjectives'],
                    'damageDealtToTurrets' : participant['damageDealtToTurrets'],
                    'totalTimeSpentDead' : participant['totalTimeSpentDead'],
                    'totalHeal' : participant['totalHeal'],
                    'totalHealsOnTeammates' : participant['totalHealsOnTeammates'],
                    'saveAllyFromDeath' : participant['challenges'].get('saveAllyFromDeath'),
                    'allInPings' : participant['allInPings'],
                    'assistMePings' : participant['assistMePings'],
                    'basicPings' : participant['basicPings'],
                    'commandPings' : participant['commandPings'],
                    'dangerPings' : participant['dangerPings'],
                    'enemyMissingPings' : participant['enemyMissingPings'],
                    'enemyVisionPings' : participant['enemyVisionPings'],
                    'getBackPings' : participant['getBackPings'],
                    'holdPings' : participant['holdPings'],
                    'needVisionPings' : participant['needVisionPings'],
                    'onMyWayPings' : participant['onMyWayPings'],
                    'pushPings' : participant['pushPings'],
                    'visionClearedPings' : participant['visionClearedPings']
                })
        return participant_data
    else:
        print(f"Failure for : {match_id}, code : {response.status_code}")
        return []

# Traitement des matchs
all_matches_data = []
i = 0
for match in matches:
    i = i + 1
    prct = i / len(matches)
    print('Match number : ',i)
    print('Progress : ', (round(prct*100,2)),"%")
    match_data = process_match(match)
    all_matches_data.extend(match_data)
    time.sleep(1.3)  # Respecter la limite de taux de l'API

# Écriture dans un fichier CSV
with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/match_data_kr.csv', 'w', newline='') as file:
    if all_matches_data:
        writer = csv.DictWriter(file, fieldnames=all_matches_data[0].keys())
        writer.writeheader() 
        writer.writerows(all_matches_data)