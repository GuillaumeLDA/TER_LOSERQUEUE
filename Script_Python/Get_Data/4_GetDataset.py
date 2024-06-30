"""
Gets data from MatchIDS.
"""

#Lib
import requests
import csv
import time
import json

#API Key
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/apiKey.txt", 'r') as file:
    apiKey = file.read().strip()

#Puuids File
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/summoners_info.json", 'r') as file:
    summoners_data = json.load(file)
    summoner_puuids = [summoner['puuid'] for summoner in summoners_data]

#MatchsID File
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Match_ID.txt", 'r') as f:
    matches = f.read().splitlines()

#Get data from matchs
def process_match(match_id):
    response = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={apiKey}')
    if response.status_code == 200:
        match_data = response.json()
        metadata = match_data['metadata']
        info = match_data['info']
        
        match_id = metadata['matchId']
        participants_puuids = metadata['participants']
        GameTime = info['gameDuration'] / 60
        game_version_major = info['gameVersion'].split('.')[0]

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
        print(f"Failure for : {match_id}, Code : {response.status_code}")
        return []


all_matches_data = []
i = 0
for match in matches:
    i = i + 1
    prct = i / len(matches)
    print('Match ID : ',i)
    print('Progress : ', (round(prct*100,2)),"%")
    match_data = process_match(match)
    all_matches_data.extend(match_data)
    time.sleep(1.3)

with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/match_data.csv', 'w', newline='') as file:
    if all_matches_data:
        writer = csv.DictWriter(file, fieldnames=all_matches_data[0].keys())
        writer.writeheader() 
        writer.writerows(all_matches_data)