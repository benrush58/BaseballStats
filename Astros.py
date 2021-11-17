from TeamClass import Team
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_stats(team_df):
    for i in range(0, len(team_df.columns), 2):
        df = team_df.iloc[:, [i, i+1]]
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

    plot_stats(astros)

    astros['Reg_Rank'] = [5, 8, 2, 2, 1]
    astros['Post_Round'] = [2, np.NaN, 5, 3, 4]


if __name__ == '__main__':
    main()
