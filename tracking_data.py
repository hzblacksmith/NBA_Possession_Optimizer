import numpy as np
import pandas as pd
from copy import deepcopy


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
    result = []
    for i in lst:
        i *= mult
        result.append(i)
    return result


def get_event_time_from_events(path_events, event):
    """
    :param path_events: the file path to event json file
    :param event: the event we are interested in
    :return: the wall clock and corresponding player ID of events
    """
    events_df = pd.read_json(path_events, lines=True, encoding='latin1')
    # find all events
    events = events_df.loc[events_df['eventType'] == event]
    # find wall clock of such events
    wall_clock = events["wallClock"]
    # find corresponding player id
    player_id = events["playerId"]
    return wall_clock, player_id


def modify_xyz(df, player_flag: bool):
    """
    Match shot zone data:
    1. multiply coordinates by 10
    2. transverse x and y
    3. delete z axis
    :param df: a row of data frame to be modified
    :param player_flag: flag indicating if it is processing player
    :return:
    """
    # make a deep copy of input df
    result = deepcopy(df)
    if player_flag is True:
        for i in range(len(result)):
            pos_lst = result[i]['xyz']
            enlarged = multiply_elements_in_list(pos_lst, float(10))
            swapped = swap_positions(enlarged, 0, 1)
            swapped.pop()
            result[i]['xyz'] = swapped
    else:
        pos_lst = result['xyz']
        enlarged = multiply_elements_in_list(pos_lst, float(10))
        swapped = swap_positions(enlarged, 0, 1)
        swapped.pop()
        result['xyz'] = swapped

    return result


def get_positions_at_shot(path_tracking, path_events):
    tracking_df = pd.read_json(path_tracking, lines=True, encoding='latin1')
    # retrieve wall clock of shots
    wall_clock = list(get_event_time_from_events(path_events, 'SHOT')[0])
    # retrieve all shot rows
    shot_event_row = tracking_df[tracking_df.wallClock.isin(wall_clock)]
    # print(shot_event_row.awayPlayers)
    lst = []
    for i in range(len(shot_event_row)):
        away_players_raw = shot_event_row.awayPlayers.iloc[i]
        away_players = modify_xyz(away_players_raw, True)
        home_players_raw = shot_event_row.homePlayers.iloc[i]
        home_players = modify_xyz(home_players_raw, True)
        ball_raw = shot_event_row.ball.iloc[i]
        # print(ball_raw)
        ball = modify_xyz(ball_raw, False)
        lst.append([away_players, home_players, ball])
    result = pd.DataFrame(lst)
    result.columns = ['away_player', 'home_player', 'ball']
    return result
    # print(pd.read_json(shot_row.awayPlayers, lines=True, encoding='latin1'))




bos_1_events = "Player Tracking/CLEBOS/2017051702_nba-bos_EVENTS.jsonl"
bos_1_track = "Player Tracking/CLEBOS/2017051702_nba-bos_TRACKING.jsonl"

print(get_positions_at_shot(bos_1_track, bos_1_events))
# print(get_shots_time_from_events(bos_1_events)[0])