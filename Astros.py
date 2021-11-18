from TeamClass import Team
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def plot_stats(team_df):
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i + 1]]
        sns.scatterplot(data=df)
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


def plot_summary(stats_df):
    sns.scatterplot(data=stats_df)
    plt.show()


def normalize(df):
    index = df.index
    cols = df.columns
    scaler = MinMaxScaler()
    df = scaler.fit_transform(df.to_numpy())
    df = pd.DataFrame(df, index=index, columns=cols)
    return df


def main():
    """
    astros15 = Team('HOU', '2015')
    astros16 = Team('HOU', '2016')
    astros17 = Team('HOU', '2017')
    astros18 = Team('HOU', '2018')
    astros19 = Team('HOU', '2019')

    teams = [astros15, astros16, astros17, astros18, astros19]

    teams_stats = calculate_team_stats(teams)

    astros = pd.DataFrame(teams_stats)

    astros.replace(0.0, np.NaN, inplace=True)
    astros.replace('No player BAs found', np.NaN, inplace=True)
    astros.replace('No player HRs found', np.NaN, inplace=True)
    astros.to_csv('Astros.csv')
    """

    astros = pd.read_csv('Astros.csv', index_col=0)
    astros = astros.swapaxes('index', 'columns')

    print(astros)

    # plot_stats(astros)

    astros_reg_pitch = astros[['Reg_ERA', 'Reg_HRA_avg']]
    astros_reg_bat = astros[['Reg_BA', 'Reg_HR_avg']]

    astros_reg_pitch = astros_reg_pitch.apply(lambda x: 1 / x)
    astros_reg = pd.concat([astros_reg_bat, astros_reg_pitch], axis=1)
    astros_reg['Reg_Rank'] = [0.2, 0.125, 0.5, 0.5, 1]

    astros_reg_scaled = normalize(astros_reg)

    astros_reg_scaled['Pred_Rank'] = astros_reg_scaled['Reg_BA'] * 0.15 + astros_reg_scaled['Reg_HR_avg'] * 0.6 + \
                                     astros_reg_scaled['Reg_ERA'] * 0.15 + astros_reg_scaled['Reg_HRA_avg'] * 0.1
    print(astros_reg_scaled)
    plot_summary(astros_reg_scaled)

    astros_post_pitch = astros[['Post_ERA', 'Post_HRA_avg']]
    astros_post_bat = astros[['Post_BA', 'Post_HR_avg']]
    astros_post_pitch = astros_post_pitch.apply(lambda x: 1 / x)
    astros_post = pd.concat([astros_post_bat, astros_post_pitch], axis=1)
    astros_post['Post_Round'] = [2, np.NaN, 5, 3, 4]

    astros_post_scaled = normalize(astros_post)

    astros_post_scaled['Pred_Round'] = astros_post_scaled['Post_BA'] * 0.15 + astros_post_scaled['Post_HR_avg'] * 0.1 + \
                                     astros_post_scaled['Post_ERA'] * 0.7 + astros_post_scaled['Post_HRA_avg'] * 0.1

    print(astros_post_scaled)

    plot_summary(astros_post_scaled)

    astros_overall = pd.concat([astros_reg_scaled[['Reg_Rank', 'Pred_Rank']], astros_post_scaled[['Post_Round', 'Pred_Round']]], axis=1)

    print(astros_overall)

    plot_summary(astros_overall)


if __name__ == '__main__':
    main()
