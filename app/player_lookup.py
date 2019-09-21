"""

Translate NBA player_id or second_spectrum id into player name


"""

import pandas as pd 
import dash_html_components as html

# box_scores = pd.read_csv("Basketball/Box_Scores.csv", compression='gzip', encoding='latin1')
ss_nba = pd.read_csv("../Basketball/Player_Tracking/SS_to_NBA_Player_Map.csv")

file_names = [
    # 'cle_bos_shot.csv',
    'gsw_cle_shot.csv',
    'gsw_sas_shot.csv',
]

players_df = pd.read_csv("../Data_supplement/Shot_zones_playoffs_raw/" + 'cle_bos_shot.csv')
for file_name in file_names:
    df = pd.read_csv("../Data_supplement/Shot_zones_playoffs_raw/" + file_name)

    players_df = pd.concat([players_df, df])


more_file_names = [
    'bos_shot_1617.csv',
    'cle_shot_1617.csv',
    'gsw_shot_1617.csv',
    'sas_shot_1617.csv'
]

for more_file_name in more_file_names:
    df = pd.read_csv("../Data_supplement/Shot_zones_reg_season/" + more_file_name)

    players_df = pd.concat([players_df, df])

# players_df = pd.read_csv("../Data_supplement/player_info_1617.csv")

players_df = players_df[['PLAYER_ID', 'PLAYER_NAME']]

players_df = players_df.drop_duplicates(['PLAYER_ID', 'PLAYER_NAME'])


                                      
players_info_df = pd.read_csv("../Data_supplement/player_info_1617.csv")
players_info_df = players_info_df[['PLAYER_ID', 'PLAYER_NAME']]

players_df = pd.concat([players_df, players_info_df])


players_df = players_df.merge(ss_nba, left_on = 'PLAYER_ID',
                                      right_on = 'NBA_ID')


ss_id_to_names = {}
nba_id_to_names = {}
for _, row in players_df.iterrows():
    ss_id_to_names[row['SS_ID']] = row['PLAYER_NAME']
    nba_id_to_names[row['NBA_ID']] = row['PLAYER_NAME']

print(ss_id_to_names)
print(len(ss_id_to_names))

ss_nba_ids = set(ss_nba['NBA_ID'].unique())

nba_nba_ids = set(players_df['PLAYER_ID'].unique())

print(len(ss_nba_ids - nba_nba_ids))