# Credit to: http://savvastjortjoglou.com/nba-shot-sharts.html

# But the error is "A connection attempt failed because the connected party did not
# properly respond after a period of time, or established connection failed because
# connected host has failed to respond"

import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import nbashots as nba


shot_chart_url = 'https://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=' \
                 '&LeagueID=00&LastNGames=0&TeamID=0&PlayerPosition=&Location=&Outcome=' \
                 '&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=' \
                 '&RangeType=&Season=2016-17&AheadBehind=&PlayerID=201935&EndRange=&VsDivision=' \
                 '&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=' \
                 '&SeasonType=Regular+Season&SeasonSegment=&GameID='

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/'
                         '537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# Get the webpage containing the data
response = requests.get(shot_chart_url)
# Grab the headers to be used as column headers for our DataFrame
# headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart data
shots = response.json()['resultSets'][0]['rowSet']

shot_df = pd.DataFrame(shots, columns=headers)

print(shot_df.head())