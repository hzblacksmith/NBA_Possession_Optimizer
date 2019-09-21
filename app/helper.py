from copy import deepcopy
import ast
import pandas as pd

def modify_xyz(df, player_flag: bool):
    """
    Match shot zone data:
    1. multiply coordinates by 10
    2. transverse x and y
    3. delete z axis
    :param df: a row of data frame to be modified
    :param player_flag: flag indicating if it is processing player
    :return: a deep copy of modified df
    """
    # make a deep copy of input df
    result = deepcopy(df)
    if player_flag is True:
        for i in range(len(result)):
            pos_lst = result[i]['xyz']
            # multiply coordinates by 10
            enlarged = multiply_elements_in_list(pos_lst, float(10))
            # swap x and y
            swapped = swap_positions(enlarged, 0, 1)
            swapped.pop()
            result[i]['xyz'] = swapped
    else:
        pos_lst = result['xyz']
        enlarged = multiply_elements_in_list(pos_lst, float(10))
        swapped = swap_positions(enlarged, 0, 1)
        # some ball xyz only has two elements... cost tons of time
        if len(swapped) == 3:
            swapped.pop()
        result['xyz'] = swapped
    return result


def map_to_shot_zone_xy(df, player_flag: bool):
    """
    map to shot zone coordinate position
    :param df:
    :param player_flag: whether it is player or ball position
    :return: modified dataframe
    """
    result = deepcopy(modify_xyz(df, player_flag))
    if player_flag is True:
        for i in range(len(result)):
            pos_lst = result[i]['xyz']
            if pos_lst[1] < 0:
                pos_lst[1] += 422.5
            elif pos_lst[1] >= 0:
                pos_lst[0] *= -1
                pos_lst[1] = 422.5 - pos_lst[1]

    else:
        pos_lst = result['xyz']
        if pos_lst[1] < 0:
            pos_lst[1] += 422.5
        elif pos_lst[1] >= 0:
            pos_lst[0] *= -1
            pos_lst[1] = -1 * pos_lst[1] + 422.5
    return result


def swap_positions(lst, pos1, pos2):
    """
    :param lst: target list
    :param pos1: first position
    :param pos2: second position
    :return: the list with element at pos1 and pos2 swapped
    """
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
    return lst

def multiply_elements_in_list(lst, mult):
    """
    :param lst: target list
    :param mult: number to be multiplied by
    :return:
    """
    result = []
    for i in lst:
        i *= mult
        result.append(i)
    return result

def get_player_routes(df):
    """
    Summarize time-series coordinates into player routes
    """
    off_team = int(df['team_possession'].iloc[0])
    player_routes = {}     # map player_id to routes     

    if off_team == 0:      # away team on offense
        off_team = 'awayPlayers'
    else:     # home team on offense
        off_team = 'homePlayers'

    players = df[off_team].iloc[0]
    players = ast.literal_eval(players)
    
    for player in players:
        player_routes[player['playerId']] = {'X':[], 'Y':[]}
    
    for _, row in df.iterrows():
        
        player_locs = row[off_team]
        player_locs = ast.literal_eval(player_locs)
        player_locs = map_to_shot_zone_xy(player_locs, player_flag=True)
        # print(player_locs)
        
        for player in player_locs:
            player_routes[player['playerId']]['X'].append(player['xyz'][0])
            player_routes[player['playerId']]['Y'].append(player['xyz'][1])

    return player_routes