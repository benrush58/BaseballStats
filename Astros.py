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


def plot_summary(stats_df):
    """
    name: plot_summary
    parameters: stats_df, a data frame
    returns: none, a plot
    """
    """ Scatterplot of the summary statistics for the team across different years """
    sns.scatterplot(data=stats_df)
    plt.legend(bbox_to_anchor=(.15, 1), loc='upper left', borderaxespad=0)
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


def main():
    # reading data from appropriate team csv
    astros = pd.read_csv('Astros.csv', index_col=0)
    astros = astros.swapaxes('index', 'columns')

    # plotting BA, ERA, HR, HRA
    plot_stats(astros)

    # creating new dataframes based on pitching vs batting stats (regular season)
    astros_reg_pitch = astros[['Reg_ERA', 'Reg_HRA_avg']]
    astros_reg_bat = astros[['Reg_BA', 'Reg_HR_avg']]

    # taking inverse of pitching stats to help with normalization
    astros_reg_pitch = astros_reg_pitch.apply(lambda x: 1 / x)

    # recombining the dataframes and adding inverse rank based on winning percentage/standings
    astros_reg = pd.concat([astros_reg_bat, astros_reg_pitch], axis=1)
    astros_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    # normalizing all of the regular season values
    astros_reg_scaled = normalize(astros_reg)

    # predicting the standing of the team based on the 4 stats (numbers chosen based on the visualization)
    astros_reg_scaled['Pred_Rank'] = astros_reg_scaled['Reg_BA'] * 0.15 + astros_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                     astros_reg_scaled['Reg_ERA'] * 0.15 + astros_reg_scaled['Reg_HRA_avg'] * 0.1

    # plotting all of the normalized stats with the actual and predicted rank
    plot_summary(astros_reg_scaled)

    # same process for the post season
    astros_post_pitch = astros[['Post_ERA', 'Post_HRA_avg']]
    astros_post_bat = astros[['Post_BA', 'Post_HR_avg']]
    astros_post_pitch = astros_post_pitch.apply(lambda x: 1 / x)
    astros_post = pd.concat([astros_post_bat, astros_post_pitch], axis=1)

    # Postseason round in which the Astros lost in the playoffs (or 5 if they won the world series)
    astros_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    # normalize all the postseason values
    astros_post_scaled = normalize(astros_post)

    # predicting post season elimination round based off the 4 stats (numbers chosen based off visualization)
    astros_post_scaled['Pred_Round'] = astros_post_scaled['Post_BA'] * 0.15 + astros_post_scaled['Post_HR_avg'] * 0.1 + \
                                     astros_post_scaled['Post_ERA'] * 0.7 + astros_post_scaled['Post_HRA_avg'] * 0.1

    # plotting all of the normalized stats with the actual and predicted elimination round
    plot_summary(astros_post_scaled)

    # creating dataframe of the actual and predicted ranks and rounds for each season
    astros_overall = pd.concat([astros_reg_scaled[['Reg_Rank', 'Pred_Rank']], astros_post_scaled[['Post_Round', 'Pred_Round']]], axis=1)

    # plotting the actual and predicted ranks and rounds for each season
    plot_summary(astros_overall)


if __name__ == '__main__':
    main()
