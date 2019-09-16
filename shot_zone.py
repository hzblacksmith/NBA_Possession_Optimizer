import pandas as pd
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import math

# print(list(player_shot_1617_df.columns.values))
conf_fnl_team_shot_1617_df = pd.read_csv('conf_fnl_team_shot_1617.csv')
# aaron_brooks_shot_1617_df = pd.read_csv('player_shot_chart_1617.csv')
# bos_shot_1617_df = player_shot_1617_df.loc[(player_shot_1617_df['TEAM_NAME'] == 'Boston Celtics')]
# cle_shot_1617_df = player_shot_1617_df.loc[(player_shot_1617_df['TEAM_NAME'] == 'Cleveland Cavaliers')]
# sas_shot_1617_df = player_shot_1617_df.loc[(player_shot_1617_df['TEAM_NAME'] == 'San Antonio Spurs')]
# gsw_shot_1617_df = player_shot_1617_df.loc[(player_shot_1617_df['TEAM_NAME'] == 'Golden State Warriors')]


def drop_half_court_shot(shot_chart_df):
    """
    :param shot_chart_df
    :return: df with over half-court shots dropped
    """
    index_name = shot_chart_df[shot_chart_df['LOC_Y'] > 422.5].index
    shot_chart_df.drop(index_name, inplace=True)


drop_half_court_shot(conf_fnl_team_shot_1617_df)
# drop_half_court_shot(bos_shot_1617_df)
# drop_half_court_shot(cle_shot_1617_df)
# drop_half_court_shot(sas_shot_1617_df)
# drop_half_court_shot(gsw_shot_1617_df)
# print(sas_shot_1617_df[['LOC_X', 'LOC_Y']])


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return [rho, phi]


# for i in range(len(sas_shot_1617_df[['LOC_X', 'LOC_Y']])):
    # print(cart2pol(sas_shot_1617_df['LOC_X'].iloc[i], sas_shot_1617_df['LOC_Y'].iloc[i]))
# bos_shot_1617_df.to_csv('bos_shot_1617.csv')
# cle_shot_1617_df.to_csv('cle_shot_1617.csv')
# sas_shot_1617_df.to_csv('sas_shot_1617.csv')
# gsw_shot_1617_df.to_csv('gsw_shot_1617.csv')
# conf_fnl_team_shot_1617_df.to_csv('conf_fnl_team_shot_1617.csv')

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


# the intersect between wing_segment_a and around_the_rim arc
# (-53.35, 72.89)
wing_segment_a_y = 422.5 - wing_segment_len * math.sin(np.deg2rad(80))
wing_segment_a_x = -115 + wing_segment_len * math.cos(np.deg2rad(80))

print(wing_segment_a_x)
print(wing_segment_a_y)

# the intersect between wing_segment_b and around_the_rim arc
# (53.35, 72.89)
wing_segment_b_x = 115 - wing_segment_len * math.cos(np.deg2rad(80))
wing_segment_b_y = 422.5 - wing_segment_len * math.sin(np.deg2rad(80))

print(wing_segment_b_x)
print(wing_segment_b_y)

# the intersect between mid_range_wing_a_x and mid_range_distinction arc
# (-141.43, 85.99)
mid_range_wing_a_x = -200 + mid_range_wing_len * math.cos(np.deg2rad(35))
mid_range_wing_a_y = 127 - mid_range_wing_len * math.sin(np.deg2rad(35))

print(mid_range_wing_a_x)
print(mid_range_wing_a_y)

# the intersect between mid_range_wing_a_x and mid_range_distinction arc
# (141.43, 85.99)
mid_range_wing_b_x = 200 - mid_range_wing_len * math.cos(np.deg2rad(35))
mid_range_wing_b_y = 127 - mid_range_wing_len * math.sin(np.deg2rad(35))


def linear_function(x1, y1, x2, y2):
    """
    Credit to https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: the linear function that crosses two given points
    """
    points = [(x1, y1), (x2, y2)]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords, rcond=None)[0]
    print("Line Solution is y = {m}x + {c}".format(m=m, c=c))
    return m, c


# Line Solution is y = -5.671281819617711x + -229.69740925603654
wing_segment_a_m, wing_segment_a_c = linear_function(-115, 422.5, wing_segment_a_x, wing_segment_a_y)
# Line Solution is y = 5.671281819617711x + -229.69740925603654
wing_segment_b_m, wing_segment_b_c = linear_function(115, 422.5, wing_segment_b_x, wing_segment_b_y)

# Line Solution is y = -0.7002075382097095x + -13.041507641941902
mid_range_wing_a_m, mid_range_wing_a_c = linear_function(-200, 127, mid_range_wing_a_x, mid_range_wing_a_y)
# Line Solution is y = 0.7002075382097095x + -13.041507641941902
mid_range_wing_b_m, mid_range_wing_b_c = linear_function(200, 127, mid_range_wing_b_x, mid_range_wing_b_y)


def identify_shot_zone(df):
    """
    :param df: shot data to be classified into shot zones
    :return: a 'SHOT_ZONE' column added in df with number indicating zones
    """
    loc_x = df['LOC_X']
    loc_y = df['LOC_Y']
    # Initialize a new column 'SHOT_ZONE' with value 0
    df.insert(len(df.columns), 'SHOT_ZONE', np.NaN)
    zone = df['SHOT_ZONE']
    for idx in range(len(loc_x)):
        x = loc_x.iloc[idx]
        y = loc_y.iloc[idx]
        # around the rim
        if abs(cart2pol(x, y)[0]) <= around_the_rim_radius:
            zone.iloc[idx] = 0
        #     left corner 3
        elif x < -220 and y <= 92.5:
            zone.iloc[idx] = 9
        #     right corner 3
        elif x > 220 and y <= 92.5:
            zone.iloc[idx] = 13
        #     closer mid-range
        elif around_the_rim_radius < cart2pol(x, y)[0] <= mid_range_distinction_radius:
            # left
            if y <= wing_segment_a_m * x + wing_segment_a_c:
                zone.iloc[idx] = 1
            # mid
            elif y <= wing_segment_b_m * x + wing_segment_b_c:
                zone.iloc[idx] = 3
            #     right
            elif y > wing_segment_a_m * x + wing_segment_a_c and y > wing_segment_b_m * x + wing_segment_b_c:
                zone.iloc[idx] = 2
        # further mid-range
        elif mid_range_distinction_radius < cart2pol(x, y)[0] <= three_arc_radius and -220 <= x <= 220:
            # left baseline
            if x >= -220 and mid_range_wing_a_m * x + mid_range_wing_a_c >= y:
                zone.iloc[idx] = 4
            # right baseline
            elif x < 220 and mid_range_wing_b_m * x + mid_range_wing_b_c >= y:
                zone.iloc[idx] = 8
            #  left wing
            elif mid_range_wing_a_m * x + mid_range_wing_a_c < y <= wing_segment_a_m * x + wing_segment_a_c:
                zone.iloc[idx] = 5
            # right wing
            elif mid_range_wing_b_m * x + mid_range_wing_b_c <= y <= wing_segment_b_m * x + wing_segment_b_c:
                zone.iloc[idx] = 7
            # top
            elif wing_segment_a_m * x + wing_segment_a_c < y and wing_segment_b_m * x + wing_segment_b_c < y:
                zone.iloc[idx] = 6
        elif abs(cart2pol(x, y)[0]) > three_arc_radius and y > 92.5:
            # left wing 3
            if wing_segment_a_m * x + wing_segment_a_c >= y:
                zone.iloc[idx] = 10
            # right wing 3
            elif wing_segment_b_m * x + wing_segment_b_c >= y:
                zone.iloc[idx] = 12
            # top 3
            elif wing_segment_a_m * x + wing_segment_a_c < y and wing_segment_b_m * x + wing_segment_b_c < y:
                zone.iloc[idx] = 11


identify_shot_zone(conf_fnl_team_shot_1617_df)
print(conf_fnl_team_shot_1617_df)

plt.figure(figsize=(12, 11))
plt.scatter(conf_fnl_team_shot_1617_df.LOC_X[-10:], conf_fnl_team_shot_1617_df.LOC_Y[-10:])
plt.scatter(90, 0)
draw_court(outer_lines=True)
# Descending values along the axis from left to right
# Adjust plot limits to just fit in half court
plt.xlim(-250, 250)
# Descending values along th y axis from bottom to top
# in order to place the hoop by the top of plot
plt.ylim(422.5, -47.5)
plt.show()
# plt.savefig('shot_zone.png')

conf_fnl_team_shot_1617_df.to_csv('conf_fnl_team_shot_1617_w_shot_zone.csv')