# aggregate player --> shot zone --> FG%, made shots, attempt shots

"""
+------------+-------------------+---------+-----------------+--------------------+
|   Player   |   Shot_zone_idx   |   FG%   |  # Made Shots   | # attempted shots  |
"""

import pandas as pd



file_names = [
    "bos_shot_1617_w_shot_zone.csv",
    "cle_shot_1617_w_shot_zone.csv",
    "gsw_shot_1617_w_shot_zone.csv",
    "sas_shot_1617_w_shot_zone.csv"
]


for file_name in file_names:

    df = pd.read_csv(file_name)


    result = df.groupby(['PLAYER_ID','SHOT_ZONE'],as_index=False).agg({
        'SHOT_ATTEMPTED_FLAG' : 'sum',
        'SHOT_MADE_FLAG' : 'sum'
    })

    result = result.rename(columns={
        'SHOT_ATTEMPTED_FLAG' : 'NUM_SHOTS_ATTEMPTED',
        'SHOT_MADE_FLAG' : 'NUM_SHOTS_MADE'
    })

    result['FG_pctg'] = result['NUM_SHOTS_MADE'] / result['NUM_SHOTS_ATTEMPTED']

    result.to_csv('Player_shot_zones_agg/' + file_name[0:8] + '_agg.csv')
    
