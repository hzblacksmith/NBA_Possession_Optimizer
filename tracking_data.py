import numpy as np
import pandas as pd
from copy import deepcopy
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt


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


def get_event_time_player_from_events(path_events, event):
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

# from now on we work on the copy to not to mutate the original df
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


def map_to_shot_zone_xy(df, player_flag: bool):
    """
    map to shot zone coordinate position
    :param df:
    :param player_flag: whether it is player or ball position
    :return: modified dataframe
    """
    result = modify_xyz(df, player_flag)
    if player_flag is True:
        for i in range(len(result)):
            pos_lst = result[i]['xyz']
            if pos_lst[1] < 0:
                pos_lst[0] = -1 * pos_lst[0]
                pos_lst[1] += 422.5
            elif pos_lst[1] >= 0:
                pos_lst[1] = -1 * pos_lst[1] + 422.5
    else:
        pos_lst = result['xyz']
        if pos_lst[1] < 0:
            pos_lst[0] = -1 * pos_lst[0]
            pos_lst[1] += 422.5
        elif pos_lst[1] >= 0:
            pos_lst[1] = -1 * pos_lst[1] + 422.5
    return result


def get_positions_at_shot(path_tracking, path_events):
    """

    :param path_tracking:
    :param path_events:
    :return: a data frame containing shooter as well as away player, home player and ball positions
    """
    tracking_df = pd.read_json(path_tracking, lines=True, encoding='latin1')
    # retrieve wall clock of shots
    wall_clock = list(get_event_time_player_from_events(path_events, 'SHOT')[0])
    shooters = list(get_event_time_player_from_events(path_events, 'SHOT')[1])
    # retrieve all shot rows
    shot_event_row = tracking_df[tracking_df.wallClock.isin(wall_clock)]
    # print(shot_event_row.awayPlayers)
    lst = []
    for i in range(len(shot_event_row)):
        away_players_raw = shot_event_row.awayPlayers.iloc[i]
        away_players = map_to_shot_zone_xy(away_players_raw, True)
        home_players_raw = shot_event_row.homePlayers.iloc[i]
        home_players = map_to_shot_zone_xy(home_players_raw, True)
        ball_raw = shot_event_row.ball.iloc[i]
        ball = map_to_shot_zone_xy(ball_raw, False)
        shooter = shooters[i]
        lst.append([shooter, away_players, home_players, ball])
    result = pd.DataFrame(lst)
    result.columns = ['shooter', 'away_players', 'home_players', 'ball']
    return result


srt_path = "C:\\Users\lilif\Desktop\\NBA Hackathon\\2019 Basketball Analytics\Basketball\Player Tracking"

bos_1_events = srt_path + "\CLEBOS\\2017051702_nba-bos_EVENTS.jsonl"
bos_1_track = srt_path + "\CLEBOS\\2017051702_nba-bos_TRACKING.jsonl"
bos_2_events = srt_path + "\CLEBOS\\2017051702_nba-bos_EVENTS.jsonl"

bos_2_events = srt_path + "\CLEBOS\\2017051702_nba-bos_EVENTS.jsonl"
bos_2_track = srt_path + "\CLEBOS\\2017051702_nba-bos_TRACKING.jsonl"

cle_3_events = srt_path + "\CLEBOS\\2017052106_nba-cle_EVENTS.jsonl"
cle_3_track = srt_path + "\CLEBOS\\2017052106_nba-cle_TRACKING.jsonl"

sas_3_events = srt_path + "\SASGSW\\2017052027_nba-sas_EVENTS.jsonl"
sas_3_track = srt_path + "\SASGSW\\2017052027_nba-sas_TRACKING.jsonl"
bos_1_shot = get_positions_at_shot(bos_1_track, bos_1_events)


def calculate_closest_distance(player_pos, opponent):
    """

    :param player_pos: [x, y] position of player
    :param opponent: a list of opponent players
    :return: the closest distance between opponent player and player
    """
    flag = np.inf
    for i in range(len(opponent)):
        dist = np.sqrt((player_pos[0] - opponent[i]['xyz'][0]) ** 2 +
                       (player_pos[1] - opponent[i]['xyz'][1]) ** 2)
        if dist < flag:
            flag = dist
    return flag


def closest_dist(path_track, path_events):
    df = get_positions_at_shot(path_track, path_events)
    shooter = df['shooter']
    away = df['away_players']
    # print(away)
    home = df['home_players']
    dist = []
    for i in range(len(shooter)):
        for p in range(5):
            if shooter[i] == away[i][p]['playerId']:
                shooter_pos = away[i][p]['xyz']
                d = calculate_closest_distance(shooter_pos, home[i])
            elif shooter[i] == home[i][p]['playerId']:
                shooter_pos = home[i][p]['xyz']
                d = calculate_closest_distance(shooter_pos, away[i])
        dist.append(d)
    df['shortest_dist'] = dist
    print(df.shortest_dist.loc[df['shortest_dist'] > 40.0])


# closest_dist(bos_1_track, bos_1_events)
# get_positions_at_shot(bos_1_track, bos_1_events).to_csv("bos_1_shot.csv")


# the radius of three pointer arc
three_arc_radius = 475 / 2.0

# shot zone line width
lw_shot_zone = 2

# radius of shot zone arc around the rim
around_the_rim_radius = 90.0
# the width of corner 3s area
corner_segment_len = 30.0
# the line to separate baseline and wing mid range
mid_range_wing_len = 71.5
# the line that separates top key and wing
wing_segment_len = 355.0
# the radius of the arc that separates mid range
mid_range_distinction_radius = np.sqrt(160**2 + 290 ** 2) / 2.0


def draw_court(ax=None, color='black', lw=4, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 139, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 139, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), three_arc_radius * 2, three_arc_radius * 2, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Shot zone segmentation

    # the arc for around the rim area
    around_the_rim = Arc((0, 0), around_the_rim_radius * 2, around_the_rim_radius * 2,
                         theta1=-40, theta2=220, linewidth=lw_shot_zone, color="red")

    # Corner 3 segmentation line

    corner_segment_a = Rectangle((-250, 92.5), corner_segment_len, 0, linewidth=lw_shot_zone,
                                 color="red")
    corner_segment_b = Rectangle((220, 92.5), corner_segment_len, 0, linewidth=lw_shot_zone,
                                 color="red")

    # the arc to distinguish two non-paint

    mid_range_distinction = Arc((0, 0), mid_range_distinction_radius * 2,
                                mid_range_distinction_radius * 2,
                                theta1=-20, theta2=200, linewidth=lw_shot_zone, color="red")

    # Wing 3 segmentation line
    wing_segment_a = Rectangle((-115, 422.5), wing_segment_len, 0, -80, linewidth=lw_shot_zone,
                               color="red")
    wing_segment_b = Rectangle((115, 422.5), wing_segment_len, 0, 260, linewidth=lw_shot_zone,
                               color="red")

    # the line between base mid-range and wing mid-range
    mid_range_wing_a = Rectangle((-200, 127), mid_range_wing_len, 0, -35, linewidth=lw_shot_zone,
                                 color="red")
    mid_range_wing_b = Rectangle((200, 127), mid_range_wing_len, 0, -145, linewidth=lw_shot_zone,
                                 color="red")

    # add shot zone lines to the graph
    court_elements.append(corner_segment_a)
    court_elements.append(corner_segment_b)
    court_elements.append(mid_range_distinction)
    court_elements.append(around_the_rim)
    court_elements.append(wing_segment_a)
    court_elements.append(wing_segment_b)
    court_elements.append(mid_range_wing_a)
    court_elements.append(mid_range_wing_b)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

plt.figure(figsize=(12, 11))
plt.scatter(get_positions_at_shot(bos_1_track, bos_1_events).away_players[0][4]['xyz'][0],
            get_positions_at_shot(bos_1_track, bos_1_events).away_players[0][4]['xyz'][1])
draw_court(outer_lines=True)
# Descending values along the axis from left to right
# Adjust plot limits to just fit in half court
plt.xlim(-250, 250)
# Descending values along th y axis from bottom to top
# in order to place the hoop by the top of plot
plt.ylim(422.5, -47.5)
# plt.show()
print(get_positions_at_shot(bos_1_track, bos_1_events).away_players[0][4]['xyz'][0],
      get_positions_at_shot(bos_1_track, bos_1_events).away_players[0][4]['xyz'][1])