from TeamClass import Team
from PlayerClass import Player
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

"""
Overperformed: 2015 Astros, 2016 Dodgers, 2017 Yankees, 2017 Astros, 2018 Dodgers

Underperformed: 2015 Yankees, 2015 Dodgers, 2017 Dodgers, 2019 Astros, 2019 Dodgers

Correctly performed: 2016 Red Sox, 2017 Red Sox, 2018 Red Sox, 2018 Yankees, 2018 Astros, 2019 Yankees

Didn't make playoffs: 2015 Red Sox, 2016 Yankees, 2016 Astros, 2019 Red Sox
"""


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


def get_team_stats(teams):
    """
    name: get_team_stats
    parameters: teams, a list of the years of teams
    returns: a nested dictionary with relevent statistics
    """
    """ Calculates the stats we are using for regular season and post season.
    Returns a dictionary with name of the stats as keys and the stat value as values """

    years = {}

    for team in teams:
        years[team.id + team.year] = {"reg_batavg": team.reg_ba(), "post_batavg": team.post_ba(),
                                      "reg_era": team.reg_era(),
                                      "post_era": team.post_era(), "reg_hra": team.reg_hra(),
                                      "post_hra": team.post_hra(),
                                      "pitch_reg_hra": team.pitch_reg_hra(), "pitch_post_hra": team.pitch_post_hra()}
    return years


def main():
    # No playoff appearance (78-84, not good, last in AL East)
    redsox15 = Team('BOS', "2015")
    # Eliminated in first round (93-69, first in AL East, 3rd in AL, projected to lose in the first round)
    redsox16 = Team('BOS', "2016")
    # Eliminated in first round (93-69 again, first in AL East, 3rd in AL, projected to lose in the first round
    redsox17 = Team('BOS', "2017")
    # Won world series (108-54, first  in AL East, 1st in all of baseball, projected to win the world series
    redsox18 = Team('BOS', "2018")
    # Not close to playoffs, could be interesting to examine the fall off
    redsox19 = Team('BOS', "2019")

    teams = [redsox15, redsox16, redsox17, redsox18, redsox19]
    stats = get_team_stats(teams)
    print(stats)

    redsox = pd.read_csv('redsox.csv', index_col=0)
    redsox = redsox.swapaxes('index', 'columns')
    plot_stats(redsox)

    # creating new dataframes based on pitching vs batting stats (regular season)
    sox_reg_pitch = redsox[['Reg_ERA', 'Reg_HRA_avg']]
    sox_reg_bat = redsox[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    sox_reg_pitch = sox_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    sox_reg = pd.concat([sox_reg_bat, sox_reg_pitch], axis=1)
    sox_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    # normalizing all of the values
    sox_reg_scaled = normalize(sox_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    sox_reg_scaled['Pred_Rank'] = sox_reg_scaled['Reg_BA'] * 0.15 + sox_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                  sox_reg_scaled['Reg_ERA'] * 0.15 + sox_reg_scaled['Reg_HRA_avg'] * 0.1

    print(sox_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(sox_reg_scaled)

    # same process for the post season
    sox_post_pitch = redsox[['Post_ERA', 'Post_HRA_avg']]
    sox_post_bat = redsox[['Post_BA', 'Post_HR_avg']]
    sox_post_pitch = sox_post_pitch.apply(lambda x: 1 / x)
    sox_post = pd.concat([sox_post_bat, sox_post_pitch], axis=1)

    # instead of rank, I used round to represent the round they lost in the playoffs (or 5 if they won world series)
    sox_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    sox_post_scaled = normalize(sox_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    sox_post_scaled['Pred_Round'] = sox_post_scaled['Post_BA'] * 0.15 + sox_post_scaled['Post_HR_avg'] * 0.1 + \
                                    sox_post_scaled['Post_ERA'] * 0.7 + sox_post_scaled['Post_HRA_avg'] * 0.1

    print(sox_post_scaled)

    plot_summary(sox_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    sox_overall = pd.concat([sox_reg_scaled[['Reg_Rank', 'Pred_Rank']], sox_post_scaled[['Post_Round', 'Pred_Round']]],
                            axis=1)

    print(sox_overall)

    plot_summary(sox_overall)


if __name__ == '__main__':
    main()
