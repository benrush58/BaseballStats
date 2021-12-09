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
    # Teams that underperformed
    yanks15 = Team('NYA', '2015')
    dodgers15 = Team('LAN', '2015')
    dodgers17 = Team('LAN', '2017')
    astros19 = Team('HOU', '2019')
    dodgers19 = Team('LAN', '2019')
    under_teams = [yanks15, dodgers15, dodgers17, astros19, dodgers19]

    under_stats = get_team_stats(under_teams)
    print(under_stats)
    under = pd.read_csv("data_csv/Unders.csv", index_col=0)
    under = under.swapaxes('index', 'columns')
    plot_stats(under)

    # creating new dataframes based on pitching vs batting stats (regular season)
    under_reg_pitch = under[['Reg_ERA', 'Reg_HRA_avg']]
    under_reg_bat = under[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    under_reg_pitch = under_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    under_reg = pd.concat([under_reg_bat, under_reg_pitch], axis=1)
    under_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    # normalizing all of the values
    under_reg_scaled = normalize(under_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    under_reg_scaled['Pred_Rank'] = under_reg_scaled['Reg_BA'] * 0.15 + under_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                  under_reg_scaled['Reg_ERA'] * 0.15 + under_reg_scaled['Reg_HRA_avg'] * 0.1

    print(under_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(under_reg_scaled)

    # same process for the post season
    under_post_pitch = under[['Post_ERA', 'Post_HRA_avg']]
    under_post_bat = under[['Post_BA', 'Post_HR_avg']]
    under_post_pitch = under_post_pitch.apply(lambda x: 1 / x)
    under_post = pd.concat([under_post_bat, under_post_pitch], axis=1)

    # instead of rank, I used round to represent the round they lost in the playoffs (or 5 if they won world series)
    under_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    under_post_scaled = normalize(under_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    under_post_scaled['Pred_Round'] = under_post_scaled['Post_BA'] * 0.15 + under_post_scaled['Post_HR_avg'] * 0.1 + \
                                    under_post_scaled['Post_ERA'] * 0.7 + under_post_scaled['Post_HRA_avg'] * 0.1

    print(under_post_scaled)

    plot_summary(under_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    under_overall = pd.concat([under_reg_scaled[['Reg_Rank', 'Pred_Rank']], under_post_scaled[['Post_Round', 'Pred_Round']]],
                            axis=1)

    print(under_overall)

    plot_summary(under_overall)


if __name__ == '__main__':
    main()