"""
The code uses the League of Legends API to get the IDs of players
ranked in different divisions, from Challenger to Gold
"""

#Library 
import requests
import time


#API Key (private)
with open("/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/apiKey.txt", 'r') as file:
    apiKey = file.read().strip()


def get_ranked_id(url_rank, apiKey, output):
    """
    Get ranked player IDs in League of Legends using the Riot Games API. 
    Filters players with 100+ games
    """
    url = f"https://euw1.api.riotgames.com/lol/league/v4/{url_rank}"
    response = requests.get(f"{url}api_key={apiKey}")

    if response.status_code == 200:
        if output in ['CHALL', 'GM', 'M']:
            data = response.json()
            players = data['entries']
            n = 100
        else :
            players = response.json()
            n = 20

        filtered_players = [ 
            {'summonerId': player['summonerId'], 'leaguePoints': player['leaguePoints'], 'games': player['wins'] + player['losses']}
            for player in players if player['wins'] + player['losses'] > 100
        ]
        sorted_players = sorted(filtered_players, key=lambda x: x['leaguePoints'], reverse=True)

        filename = f"/Applications/Dossier/cours/Master MIASHS/M2/TER/Python/Data/Data For API/Summoner_id_{output}.txt"
        with open(filename, 'w') as file:
            for player in sorted_players[:n]:
                file.write(player['summonerId'] + '\n')
        time.sleep(1.3)
    else:
        print(f"Failure for {url_rank}: Code", response.status_code)
        time.sleep(1.4)


#Writing files
get_ranked_id('challengerleagues/by-queue/RANKED_SOLO_5x5?', apiKey, 'CHALL')
get_ranked_id('grandmasterleagues/by-queue/RANKED_SOLO_5x5?', apiKey, 'GM')
get_ranked_id('masterleagues/by-queue/RANKED_SOLO_5x5?', apiKey, 'M')
get_ranked_id('entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&', apiKey, 'D1')
get_ranked_id('entries/RANKED_SOLO_5x5/DIAMOND/II?page=1&', apiKey, 'D2')
get_ranked_id('entries/RANKED_SOLO_5x5/DIAMOND/III?page=1&', apiKey, 'D3')
get_ranked_id('entries/RANKED_SOLO_5x5/DIAMOND/IV?page=1&', apiKey, 'D4')
get_ranked_id('entries/RANKED_SOLO_5x5/EMERALD/I?page=1&', apiKey, 'E1')
get_ranked_id('entries/RANKED_SOLO_5x5/EMERALD/II?page=1&', apiKey, 'E2')
get_ranked_id('entries/RANKED_SOLO_5x5/EMERALD/III?page=1&', apiKey, 'E3')
get_ranked_id('entries/RANKED_SOLO_5x5/EMERALD/IV?page=1&', apiKey, 'E4')
get_ranked_id('entries/RANKED_SOLO_5x5/PLATINUM/I?page=1&', apiKey, 'P1')
get_ranked_id('entries/RANKED_SOLO_5x5/PLATINUM/II?page=1&', apiKey, 'P2')
get_ranked_id('entries/RANKED_SOLO_5x5/PLATINUM/III?page=1&', apiKey, 'P3')
get_ranked_id('entries/RANKED_SOLO_5x5/PLATINUM/IV?page=1&', apiKey, 'P4')
get_ranked_id('entries/RANKED_SOLO_5x5/GOLD/I?page=1&', apiKey, 'G1')
get_ranked_id('entries/RANKED_SOLO_5x5/GOLD/II?page=1&', apiKey, 'G2')
get_ranked_id('entries/RANKED_SOLO_5x5/GOLD/III?page=1&', apiKey, 'G3')
get_ranked_id('entries/RANKED_SOLO_5x5/GOLD/IV?page=1&', apiKey, 'G4')
