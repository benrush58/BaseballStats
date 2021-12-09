#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 15:51:29 2021

@author: Marta
"""

"""
dodgers file
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
    """ 
    name: plot_stats
    parameters: team_df, a data frame with all the team data
    returns: none, a plot 
    """
    """ Plots the 4 stats we are using on 4 different scatterplots with
    regular season and post season differentiated by color """
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i + 1]]
        sns.scatterplot(data=df)
        plt.show()


def calculate_team_stats(teams):
    """ 
    name: calculate_team_stats
    parameters: teams, a list of the years of teams
    returns: a nested dictionary with relevent statistics
    """    
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

def get_team_stats(teams):
    """
    name: get_team_stats
    parameters: teams, a list 
    returns: a differently formatted dictionary of data
    """
    # Program intakes list of teams and gets all stats for the teams

    years = {}

    for team in teams:

        years[team.id + team.year] = {"reg_batavg": team.reg_ba(), "post_batavg": team.post_ba(), "reg_era": team.reg_era(),
                            "post_era": team.post_era(), "reg_hra": team.reg_hra(), "post_hra": team.post_hra(),
                            "pitch_reg_hra": team.pitch_reg_hra(), "pitch_post_hra": team.pitch_post_hra()}
    return years

def plot_summary(stats_df):
    """ 
    name: plot_summary
    parameters: stats_df, a data frame
    returns: none, a plot
    """
    """ Scatterplot of the summary statistics for the team across different years """
    sns.lineplot(data=stats_df)
    plt.show()


def normalize(df):
    """ 
    name: normalize
    paramater: df, a data frame
    returns: df, a data frame with normalized values
    """
    """ Scales all of the columns in the dataframe to values between 0 and 1 """
    index = df.index
    cols = df.columns
    scaler = MinMaxScaler()
    df = scaler.fit_transform(df.to_numpy())
    df = pd.DataFrame(df, index=index, columns=cols)
    return df



if __name__ == "__main__":
    dodgers15 = Team('LAN', '2015')
    dodgers16 = Team('LAN', '2016')
    dodgers17 = Team('LAN', '2017')
    dodgers18 = Team('LAN', '2018')
    dodgers19 = Team('LAN', '2019')

    teams = [dodgers15, dodgers16, dodgers17, dodgers18, dodgers19]
    """
    some stats I pulled from online just for reference
    2015: 92-70, 0.568, lost to Mets in NL series
    2016: 91-71, 0.562, lost to Cubs in NL championship series
    2017: 104-58, 0.642, lost in world series to Astros
    2018: 92-71, 0.564, lost in world series to Red Sox
    2019: 106-56, 0.654, lost in NL series to Nationals
    """
    # make a csv wtih just Dodgers, commented out so it runs faster and uses
    #the new csv not the big one
    """
    teams_stats = calculate_team_stats(teams)
    dodgers = pd.DataFrame(teams_stats)
    dodgers.replace(0.0, np.NaN, inplace=True)
    dodgers.replace('No player BAs found', np.NaN, inplace=True)
    dodgers.replace('No player HRs found', np.NaN, inplace=True)
    dodgers.to_csv('Dodgers.csv')
    
    dodgers = pd.read_csv('Dodgers.csv', index_col=0)
    dodgers = dodgers.swapaxes('index', 'columns')

    
    dodgers['Reg_Rank'] = [5, 8, 2, 2, 1]
    dodgers['Post_Round'] = [2, np.NaN, 5, 3, 4]
    """

    # reading from csv to make the process faster
    dodgers = pd.read_csv('data_csv/Dodgers.csv', index_col=0)
    dodgers = dodgers.swapaxes('index', 'columns')

    print(dodgers)

    # plotting the 4 stats
    plot_stats(dodgers)

    # creating new dataframes based on pitching vs batting stats (regular season)
    dodgers_reg_pitch = dodgers[['Reg_ERA', 'Reg_HRA_avg']]
    dodgers_reg_bat = dodgers[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    dodgers_reg_pitch = dodgers_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    dodgers_reg = pd.concat([dodgers_reg_bat, dodgers_reg_pitch], axis=1)
    #Uupdated numbers below based on overall finish in MLB
    #2015 6th 
    #2016 6th
    #2017 1st
    #2018 7th
    #2019 2nd
    dodgers_reg['Reg_Rank'] = [0.166, 0.166, 1, 0.142, 0.5]
    
    # normalizing all of the values
    dodgers_reg_scaled = normalize(dodgers_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    dodgers_reg_scaled['Pred_Rank'] = dodgers_reg_scaled['Reg_BA'] * 0.1 + dodgers_reg_scaled['Reg_HR_avg'] * 0.4 + \
                                    dodgers_reg_scaled['Reg_ERA'] * 0.4 + dodgers_reg_scaled['Reg_HRA_avg'] * 0.1

    print(dodgers_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(dodgers_reg_scaled)

    # same process for the post season
    dodgers_post_pitch = dodgers[['Post_ERA', 'Post_HRA_avg']]
    dodgers_post_bat = dodgers[['Post_BA', 'Post_HR_avg']]
    dodgers_post_pitch = dodgers_post_pitch.apply(lambda x: 1 / x)
    dodgers_post = pd.concat([dodgers_post_bat, dodgers_post_pitch], axis=1)

    # instead of rank, we used round to represent the round they lost in the playoffs (or 5 if they won world series)
    dodgers_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    dodgers_post_scaled = normalize(dodgers_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    dodgers_post_scaled['Pred_Round'] = dodgers_post_scaled['Post_BA'] * 0.1 + dodgers_post_scaled['Post_HR_avg'] * 0.4 + \
                                     dodgers_post_scaled['Post_ERA'] * 0.4 + dodgers_post_scaled['Post_HRA_avg'] * 0.1

    print(dodgers_post_scaled)

    plot_summary(dodgers_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    dodgers_overall = pd.concat([dodgers_reg_scaled[['Reg_Rank', 'Pred_Rank']], dodgers_post_scaled[['Post_Round', 'Pred_Round']]], axis=1)

    print(dodgers_overall)



