# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:46:00 2021

@author: alans
"""

"""
yanks
"""

from TeamClass import Team
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def plot_stats(team_df):
    """ Plots the 4 stats we are using on 4 different scatterplots with
    regular season and post season differentiated by color """
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i + 1]]
        sns.scatterplot(data=df)
        plt.show()


def calculate_team_stats(teams):
    """ Calculates the stats we are using for regular season and post season.
    Returns a dictionary with name of the stats as keys and the stat value as values """
    teams_stats = {}

    for team in teams:
        reg_ba = team.reg_ba()
        post_ba = team.post_ba()
        reg_era = team.reg_era()
        post_era = team.post_era()
        reg_hra = team.reg_hra()
        post_hra = team.post_hra()
        pitch_reg_hra = team.pitch_reg_hra()
        pitch_post_hra = team.pitch_post_hra()

        teams_stats[team.year] = {'Reg_BA': reg_ba, 'Post_BA': post_ba, 'Reg_HR_avg': reg_hra, 'Post_HR_avg': post_hra,
                                  'Reg_ERA': reg_era, 'Post_ERA': post_era, 'Reg_HRA_avg': pitch_reg_hra,
                                  'Post_HRA_avg': pitch_post_hra}
    return teams_stats


def plot_summary(stats_df):
    """ Scatterplot of the summary statistics for the team across different years """
    sns.lineplot(data=stats_df)
    plt.show()


def normalize(df):
    """ Scales all of the columns in the dataframe to values between 0 and 1 """
    index = df.index
    cols = df.columns
    scaler = MinMaxScaler()
    df = scaler.fit_transform(df.to_numpy())
    df = pd.DataFrame(df, index=index, columns=cols)
    return df

if __name__ == "__main__":
    yanks15 = Team('NYY', '2015')
    yanks16 = Team('NYY', '2016')
    yanks17 = Team('NYY', '2017')
    yanks18 = Team('NYY', '2018')
    yanks19 = Team('NYY', '2019')

    teams = [yanks15, yanks16, yanks17, yanks18, yanks19]
    """
    some stats I pulled from online just for reference
    2015: 87-75, lost to Astros in Wild Card
    2016: 84-78, Missed the playoffs
    2017: 91-71, lost in ALCS to Astros
    2018: 100-62, lost in ALDS to Red Sox
    2019: 103-59, lost in ALCS to Astros
    """   
    """
    teams_stats = calculate_team_stats(teams)
    yanks = pd.DataFrame(teams_stats)
    yanks.replace(0.0, np.NaN, inplace=True)
    yanks.replace('No player BAs found', np.NaN, inplace=True)
    yanks.replace('No player HRs found', np.NaN, inplace=True)
    yanks.to_csv('Yanks.csv')
    """
    
    #code below is used in Astros and Dodgers files

    # reading from csv to make the process faster
    yanks = pd.read_csv('Yanks.csv', index_col=0)
    yanks = yanks.swapaxes('index', 'columns')

    print(yanks)

    # plotting the 4 stats
    plot_stats(yanks)

    # creating new dataframes based on pitching vs batting stats (regular season)
    yanks_reg_pitch = yanks[['Reg_ERA', 'Reg_HRA_avg']]
    yanks_reg_bat = yanks[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    yanks_reg_pitch = yanks_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    yanks_reg = pd.concat([yanks_reg_bat, yanks_reg_pitch], axis=1)
    yanks_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    # normalizing all of the values
    yanks_reg_scaled = normalize(yanks_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    yanks_reg_scaled['Pred_Rank'] = yanks_reg_scaled['Reg_BA'] * 0.15 + yanks_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                    yanks_reg_scaled['Reg_ERA'] * 0.15 + yanks_reg_scaled['Reg_HRA_avg'] * 0.1

    print(yanks_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(yanks_reg_scaled)

    # same process for the post season
    yanks_post_pitch = yanks[['Post_ERA', 'Post_HRA_avg']]
    yanks_post_bat = yanks[['Post_BA', 'Post_HR_avg']]
    yanks_post_pitch = yanks_post_pitch.apply(lambda x: 1 / x)
    yanks_post = pd.concat([yanks_post_bat, yanks_post_pitch], axis=1)

    # instead of rank, I used round to represent the round they lost in the playoffs (or 5 if they won world series)
    yanks_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    yanks_post_scaled = normalize(yanks_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    yanks_post_scaled['Pred_Round'] = yanks_post_scaled['Post_BA'] * 0.15 + yanks_post_scaled['Post_HR_avg'] * 0.1 + \
                                     yanks_post_scaled['Post_ERA'] * 0.7 + yanks_post_scaled['Post_HRA_avg'] * 0.1

    print(yanks_post_scaled)

    plot_summary(yanks_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    yanks_overall = pd.concat([yanks_reg_scaled[['Reg_Rank', 'Pred_Rank']], yanks_post_scaled[['Post_Round', 'Pred_Round']]], axis=1)

    print(yanks_overall)

    plot_summary(yanks_overall)
