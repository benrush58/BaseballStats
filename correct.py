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
    # Teams that correctperformed
    redsox16 = Team('BOS', "2016")
    redsox17 = Team('BOS', "2017")
    redsox18 = Team('BOS', "2018")
    yanks18 = Team('NYA', '2018')
    astros18 = Team('HOU', '2018')
    yanks19 = Team('NYA', '2019')
    correct_teams = [redsox16, redsox17, redsox18, yanks18, astros18, yanks19]

    correct_stats = get_team_stats(correct_teams)
    print(correct_stats)
    correct = pd.read_csv("Correct.csv", index_col=0)
    correct = correct.swapaxes('index', 'columns')
    plot_stats(correct)

    # creating new dataframes based on pitching vs batting stats (regular season)
    correct_reg_pitch = correct[['Reg_ERA', 'Reg_HRA_avg']]
    correct_reg_bat = correct[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    correct_reg_pitch = correct_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    correct_reg = pd.concat([correct_reg_bat, correct_reg_pitch], axis=1)
    correct_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1, 1]

    # normalizing all of the values
    correct_reg_scaled = normalize(correct_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    correct_reg_scaled['Pred_Rank'] = correct_reg_scaled['Reg_BA'] * 0.15 + correct_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                  correct_reg_scaled['Reg_ERA'] * 0.15 + correct_reg_scaled['Reg_HRA_avg'] * 0.1

    print(correct_reg_scaled)

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(correct_reg_scaled)

    # same process for the post season
    correct_post_pitch = correct[['Post_ERA', 'Post_HRA_avg']]
    correct_post_bat = correct[['Post_BA', 'Post_HR_avg']]
    correct_post_pitch = correct_post_pitch.apply(lambda x: 1 / x)
    correct_post = pd.concat([correct_post_bat, correct_post_pitch], axis=1)

    # instead of rank, I used round to represent the round they lost in the playoffs (or 5 if they won world series)
    correct_post['Post_Round'] = [2, np.NaN, 5, 3, 4, 3]

    correct_post_scaled = normalize(correct_post)

    # again trying to predict post season success based off the 4 stats (numbers chosen based off visualization)
    correct_post_scaled['Pred_Round'] = correct_post_scaled['Post_BA'] * 0.15 + correct_post_scaled['Post_HR_avg'] * 0.1 + \
                                    correct_post_scaled['Post_ERA'] * 0.7 + correct_post_scaled['Post_HRA_avg'] * 0.1

    print(correct_post_scaled)

    plot_summary(correct_post_scaled)

    # one final comparison of the actual and predicted ranks and rounds for each season
    # (is there any correlation between the stats and actually winning?)
    correct_correctall = pd.concat([correct_reg_scaled[['Reg_Rank', 'Pred_Rank']], correct_post_scaled[['Post_Round', 'Pred_Round']]],
                            axis=1)

    print(correct_correctall)

    plot_summary(correct_correctall)


    """
    Batting average did what was expected: 
    - overperform: 1
    - underperform: 5
    ERA did what was expected:
    - overperform: 1
    - underperform: 3
    """

if __name__ == '__main__':
    main()