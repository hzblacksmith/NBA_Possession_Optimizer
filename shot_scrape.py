# Credit to: https://github.com/peaceiyi/NBAJSONCSV for how to get player ids


import requests
import pandas as pd


# We focus on 2016-17 season here
season = '2016-17'
regular_season = 'Regular+Season'
playoffs = 'Playoffs'


def url_to_df(url):
    """
    Scrape the website (json format) to dataFrame.
    :param url: json url address
    :return: the dataFrame of the json url
    """
    request_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/'
                                     '537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    # Get the webpage containing the data
    response = requests.get(url, headers=request_headers)
    # Grab the headers to be used as column headers for our DataFrame
    headers = response.json()['resultSets'][0]['headers']
    # Grab the content of the file
    content = response.json()['resultSets'][0]['rowSet']
    # Convert to dataFrame
    df = pd.DataFrame(content, columns=headers)
    return df


def url_to_shot_csv(general_stats_url, season_type):
    """
    :param general_stats_url: the url for getting general stats in order ot get player_id
    :param season_type: regular season or playoffs
    :return: a series of csv consisting of individual player's shots
    """
    df = url_to_df(general_stats_url)
    player_id_df = df['PLAYER_ID']
    for idx in range(len(player_id_df)):
        player_shot_chart_url = 'https://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=' \
                                             '&LeagueID=00&LastNGames=0&TeamID=0&PlayerPosition=&Location=&Outcome=' \
                                             '&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0' \
                                             '&ContextFilter=' \
                                             '&RangeType=&' \
                                             'Season=' + season + \
                                             '&AheadBehind=' \
                                             '&PlayerID=' + player_id_df[idx].astype(str) + \
                                             '&EndRange=&VsDivision=' \
                                             '&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=' \
                                             '&StartRange=&EndPeriod=' \
                                             '&SeasonType=' + season_type + '&SeasonSegment=&GameID='
        player_shot_chart_df = url_to_df(player_shot_chart_url)
        player_shot_chart_df.to_csv('player_shot_chart_1617_' + season_type + '_' + player_id_df[idx].astype(str) +
                                    '.csv')


player_general_stats_1617_regular_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=' \
                                '&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=' \
                                '&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0' \
                                '&OpponentTeamID=0' \
                                '&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=' \
                                '&PlayerPosition=&PlusMinus=N&Rank=N' \
                                '&Season=' + season + \
                                '&SeasonSegment=' \
                                '&SeasonType=' + regular_season + '&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0' \
                                '&VsConference=&VsDivision=&Weight='
player_general_stats_1617_playoffs_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=' \
                                '&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=' \
                                '&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0' \
                                '&OpponentTeamID=0' \
                                '&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=' \
                                '&PlayerPosition=&PlusMinus=N&Rank=N' \
                                '&Season=' + season + \
                                '&SeasonSegment=' \
                                '&SeasonType=' + playoffs + '&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0' \
                                '&VsConference=&VsDivision=&Weight='

url_to_shot_csv(player_general_stats_1617_playoffs_url, playoffs)
