"""
This code obtains the Puuids from the SumIDs, necessary to obtain the data
"""

#Lib
import requests
import time
import json
import pandas as pd

#APIKey
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/apiKey.txt", 'r') as file:
    apiKey = file.read().strip()


files = [
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_CHALL.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_GM.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_M.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_D1.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_D2.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_D3.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_D4.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_E1.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_E2.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_E3.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_E4.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_P1.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_P2.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_P3.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_P4.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_G1.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_G2.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_G3.txt',
    '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_G4.txt',
]


#Read and Combine Data
dataframes = []
for file in files:
    try:
        df = pd.read_csv(file, header=None, names=['summonerId'])
        dataframes.append(df)
    except Exception as e:
        print(f"Total number rows : {file}: {e}")


combined_df = pd.concat(dataframes, ignore_index=True)


number_of_lines = combined_df.shape[0]
print(f"s : {number_of_lines}")


output_file = '/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_Ids.txt'
combined_df.to_csv(output_file, index=False, header=False)

with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_Ids.txt", 'r') as f:
    SumIDs = f.read().splitlines()

summoners_info = []  
i = 1
for SumID in SumIDs:
    prct = i / number_of_lines
    i = i +1
    print('Progress : ', (round(prct*100,2)),"%")
    try:
        response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/' + SumID + '?api_key=' + apiKey)
        if response.status_code == 200:
            try:
                summoners_info.append(response.json())
            except json.JSONDecodeError:
                prct = i / number_of_lines
                print('Progress : ', 1-(round(prct,2)),"%")
                print('Answer:', response.text)
        else:
            print('Failure for', SumID, 'Code:', response.status_code)
            print('Answer:', response.text)
    except Exception as e:
        print('Failure for:', e)
    time.sleep(1.3)


with open('/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/summoners_info.json', 'w') as f:
    json.dump(summoners_info, f)

    