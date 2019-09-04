# 2019 NBA Hackathon Final Round
**Team: 4PPP**

**Members: Skyler Shi, Frank Li, Brandon Pollack, Faizan Abdullah**

## Quick Start

1. Download `Basketball` folder containing hackathon data from Box.
2. Move `Basketball` under this project's root directory.
3. Unzip the tracking files `CLEBOS.zip`, `CLEGSW.zip`, `SASGSW.zip` into same directory.
4. Run `Testing_Data.ipynb` to see data in pandas dataframes.

## Data Scrape
### shot_scrape.py
1. `url_to_df` function grabs json file in url and converts to pandas dataFrame. 
2. First grab the mapping from player name to player_id for 2016-17 season from https://stats.nba.com/leaders/?Season=2016-17&SeasonType=Regular%20Season page.
3. Then grab shot detail json by iterating through every player_id.
4. Each output csv file is the shot detail for every single player.

### combine_csv_to_df.py
1. Concatenate csv files to a master one.
