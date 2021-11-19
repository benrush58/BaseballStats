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
from PlayerClass import Player
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_stats(team_df):
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i+1]]
        sns.scatterplot(data=df)
        plt.show()
        
def plot_dict(data):

    for key in data.keys():
        data = data[key]
        sns.scatterplot(data)
        plt.show()
        
def calculate_team_stats(teams):
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
    win_percent = []
    ranks = []
    for team in teams:
        win_percent.append(team.return_wins())
        ranks.append(team.return_rank())

    #pretty boring bc their win percent only ranges from 0.55 to like 0.65
    plt.bar([1,2,3,4,5], win_percent)    
    plt.figure(2)
    
    #they were ranked first every single one of these years
   
    batting = []
    for team in teams:
        year = []
        for playerid, player in team.players.items():
            try:
                bat = player.return_bat_hr('2016')
            except:
                  pass
            year.append(bat)
        batting.append(year)
        
    print(batting[0])
    plt.figure(3)
    plt.scatter(range(len(batting[0])), batting[0])
    plt.show()        
    
    #find averages for batting for each year
    #ngl kind interesting bc 2015 has a much higher value than the other years
    #[6.4, 3.4363636363636365, 4.365384615384615, 3.8076923076923075, 4.3478260869565215]
    
    avgs = []
    for year in batting:
        avg = sum(year)/len(year)
        avgs.append(avg)
    #print(avgs)
    #stole the calculate_team_stats function from Astros and used it on dodgers        
   # stats = calculate_team_stats(teams)
    #print(stats)
    
    
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

    plot_stats(dodgers)

