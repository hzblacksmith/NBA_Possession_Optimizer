import pandas as pd
import glob
import os


def combine_csv_to_df(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df = (pd.read_csv(f, index_col=0) for f in all_files)
    concatenated_df = pd.concat(df, ignore_index=True)
    return concatenated_df


player_shot_1617_path = r'C:\Users\lilif\Desktop\NBA Hackathon\2019 Basketball Analytics\Basketball' \
                        r'\player_shot_chart_1617'
player_shot_1617_all_df = combine_csv_to_df(player_shot_1617_path)
player_shot_1617_all_df.to_csv("player_shot_1617_all.csv")