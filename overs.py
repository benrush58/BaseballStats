from TeamClass import Team
from PlayerClass import Player
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def plot_stats(team_df):
    """ Plots the 4 stats we are using on 4 different scatterplots with
    regular season and post season differentiated by color """
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i + 1]]
        sns.scatterplot(data=df)
        plt.show()


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



def get_team_stats(teams):
    # Program intakes list of teams and gets all stats for the teams

    years = {}

    for team in teams:
        # reg_batavg = team.reg_ba()
        # post_batavg = team.post_ba()
        # reg_era = team.reg_era()
        # post_era = team.post_era()
        # reg_hra = team.reg_hra()
        # post_hra= team.post_hra()
        # pitch_reg_hra = team.pitch_reg_hra()
        # pitch_post_hra = team.pitch_post_hra()

        years[team.id + team.year] = {"reg_batavg": team.reg_ba(), "post_batavg": team.post_ba(), "reg_era": team.reg_era(),
                            "post_era": team.post_era(), "reg_hra": team.reg_hra(), "post_hra": team.post_hra(),
                            "pitch_reg_hra": team.pitch_reg_hra(), "pitch_post_hra": team.pitch_post_hra()}
    return years



def main():
    # Teams that overperformed
    astros15 = Team('HOU', '2015')
    dodgers16 = Team('LAN', '2016')
    yanks17 = Team('NYA', '2017')
    astros17 = Team('HOU', '2017')
    dodgers18 = Team('LAN', '2018')
    over_teams = [astros15, dodgers16, yanks17, astros17, dodgers18]

    over_stats = get_team_stats(over_teams)
    print(over_stats)
    over = pd.read_csv("Overs.csv", index_col=0)
    over = over.swapaxes('index', 'columns')
    #plot_stats(over)

    # creating new dataframes based on pitching vs batting stats (regular season)
    over_reg_pitch = over[['Reg_ERA', 'Reg_HRA_avg']]
    over_reg_bat = over[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    over_reg_pitch = over_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    over_reg = pd.concat([over_reg_bat, over_reg_pitch], axis=1)
    over_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    # normalizing all of the values
    over_reg_scaled = normalize(over_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    over_reg_scaled['Pred_Rank'] = over_reg_scaled['Reg_BA'] * 0.15 + over_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                  over_reg_scaled['Reg_ERA'] * 0.15 + over_reg_scaled['Reg_HRA_avg'] * 0.1

    print(over_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(over_reg_scaled)

    # same process for the post season
    over_post_pitch = over[['Post_ERA', 'Post_HRA_avg']]
    over_post_bat = over[['Post_BA', 'Post_HR_avg']]
    over_post_pitch = over_post_pitch.apply(lambda x: 1 / x)
    over_post = pd.concat([over_post_bat, over_post_pitch], axis=1)

    # instead of rank, I used round to represent the round they lost in the playoffs (or 5 if they won world series)
    over_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    over_post_scaled = normalize(over_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    over_post_scaled['Pred_Round'] = over_post_scaled['Post_BA'] * 0.15 + over_post_scaled['Post_HR_avg'] * 0.1 + \
                                    over_post_scaled['Post_ERA'] * 0.7 + over_post_scaled['Post_HRA_avg'] * 0.1

    print(over_post_scaled)

    plot_summary(over_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    over_overall = pd.concat([over_reg_scaled[['Reg_Rank', 'Pred_Rank']], over_post_scaled[['Post_Round', 'Pred_Round']]],
                            axis=1)

    print(over_overall)

    plot_summary(over_overall)


if __name__ == '__main__':
    main()