from TeamClass import Team
from PlayerClass import Player
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

"""Goals of this research
1) Identify how each team was projected to do in the post season given their regular season record
2) Identify how each team actually did in the post season compared to the projection
3) Compare stats and players between regular season and post season with all types of graphs
4) Identify which stats and players were the most influential in their regular vs post season performance

Could be interesting to tell the story of the slow rise and the dramatic fall of the Sox in these 5 years

REFORMATING CODE:
"""

"""
Overperformed: 2015 Astros, 2016 Dodgers, 2017 Yankees, 2017 Astros, 2018 Dodgers

Underperformed: 2015 Yankees, 2015 Dodgers, 2017 Dodgers, 2019 Astros, 2019 Dodgers

Correctly performed: 2016 Red Sox, 2017 Red Sox, 2018 Red Sox, 2018 Yankees, 2018 Astros, 2019 Yankees

Didn't make playoffs: 2015 Red Sox, 2016 Yankees, 2016 Astros, 2019 Red Sox
"""

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


def replace_na(los):
    ret = []
    for x in los:
        if type(x) == str:
            if x[0] == "N":
                ret.append(0)
            else:
                ret.append(int(x))
        else:
            ret.append(x)
    return ret


def graph_regular_vs_post(regular, post, title, y):
    x_labels = ["2015", "2016", "2017", "2018", '2019']

    # Charts to make: one chart for each of the 4 stats comparing playoff to regular season performance
    post = replace_na(post)
    print("POST")
    print(post)

    width = 0.35
    bar1 = np.arange(len(x_labels))
    bar2 = [i + width for i in bar1]

    plt.bar(bar1, regular, 0.35, label="Regular Season")
    plt.bar(bar2, post, 0.35, label="Post Season")
    plt.xlabel("Year")
    plt.ylabel(y)
    plt.title(title)
    plt.xticks(bar1 + (width / 2), x_labels)
    plt.legend()
    plt.show()


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

    player = Player(First="Mookie", Last='Betts')
    # print(redsox17.reg_ba_2())
    # print(redsox17.reg_ba())
    print(redsox17.post_ba())


    # Teams that  overperformed
    astros15 = Team('HOU', '2015')
    dodgers16 = Team('LAN', '2016')
    yanks17 = Team('NYA', '2017')
    astros17 = Team('HOU', '2017')
    dodgers18 = Team('LAN', '2018')

    # Teams that underperformed
    yanks15 = Team('NYA', '2015')
    dodgers15 = Team('LAN', '2015')
    dodgers17 = Team('LAN', '2017')
    astros19 = Team('HOU', '2019')
    dodgers19 = Team('LAN', '2019')

    # Teams that performed correctly
    yanks18 = Team('NYA', '2018')
    astros18 = Team('HOU', '2018')
    yanks19 = Team('NYA', '2019')


    teams = [redsox15, redsox16, redsox17, redsox18, redsox19]
    stats = get_team_stats(teams)
    print(stats)
    #print(redsox15.trying_era())
    #print(redsox16.trying_era())
    #print(redsox17.trying_era())
    #print(redsox18.trying_era())
    #print(redsox19.trying_era())

    redsox = pd.read_csv('redsox.csv', index_col=0)
    redsox = redsox.swapaxes('index', 'columns')
    #plot_stats(redsox)

    over_teams = [astros15, dodgers16, yanks17, astros17, dodgers18]
    over_stats = get_team_stats(over_teams)
    print(over_stats)
    over = pd.read_csv("Overs.csv", index_col=0)
    over = over.swapaxes('index', 'columns')
    #plot_stats(over)

    under_teams = [yanks15, dodgers15, dodgers17, astros19, dodgers19]
    under_stats = get_team_stats(under_teams)
    print(under_stats)
    under = pd.read_csv("Unders.csv", index_col=0)
    under = under.swapaxes('index', 'columns')
    #plot_stats(under)

    correct_teams = [redsox16, redsox17, redsox18, yanks18, astros18, yanks19]
    correct_stats = get_team_stats(correct_teams)
    print(correct_stats)
    correct = pd.read_csv("Correct.csv", index_col=0)
    correct = correct.swapaxes('index', 'columns')
    plot_stats(correct)





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
    sox_overall = pd.concat([sox_reg_scaled[['Reg_Rank', 'Pred_Rank']], sox_post_scaled[['Post_Round', 'Pred_Round']]], axis=1)

    print(sox_overall)

    plot_summary(sox_overall)

"""
    # Start using graphs to represent this data
    x_labels = ["2015", "2016", "2017", "2018", '2019']

    # Charts to make: one chart for each of the 4 stats comparing playoff to regular season performance
    # print(stats["2015"]["reg_era"])
    y_label_ba_regular = [stats["2015"]["reg_batavg"], stats["2016"]["reg_batavg"], stats["2017"]["reg_batavg"],
                          stats["2018"]["reg_batavg"], stats["2019"]["reg_batavg"]]
    y_label_ba_post = [stats["2015"]["post_batavg"], stats["2016"]["post_batavg"], stats["2017"]["post_batavg"],
                       stats["2018"]["post_batavg"], stats["2019"]["post_batavg"]]
    graph_regular_vs_post(y_label_ba_regular, y_label_ba_post, "Batting Average per Season", "Batting Average")

    y_label_era_regular = [stats["2015"]["reg_era"], stats["2016"]["reg_era"], stats["2017"]["reg_era"],
                           stats["2018"]["reg_era"], stats["2019"]["reg_era"]]
    y_label_era_post = [stats["2015"]["post_era"], stats["2016"]["post_era"], stats["2017"]["post_era"],
                        stats["2018"]["post_era"], stats["2019"]["post_era"]]
    graph_regular_vs_post(y_label_era_regular, y_label_era_post, "ERA per Season", "ERA")

    y_label_hra_regular = [stats["2015"]["reg_hra"], stats["2016"]["reg_hra"], stats["2017"]["reg_hra"],
                           stats["2018"]["reg_hra"], stats["2019"]["reg_hra"]]
    y_label_hra_post = [stats["2015"]["post_hra"], stats["2016"]["post_hra"], stats["2017"]["post_hra"],
                        stats["2018"]["post_hra"], stats["2019"]["post_hra"]]
    graph_regular_vs_post(y_label_hra_regular, y_label_hra_post, "Home Run Average", "HRA")

    y_label_pitch_hra_regular = [stats["2015"]["pitch_reg_hra"], stats["2016"]["pitch_reg_hra"],
                                 stats["2017"]["pitch_reg_hra"], stats["2018"]["pitch_reg_hra"],
                                 stats["2019"]["pitch_reg_hra"]]
    y_label_pitch_hra_post = [stats["2015"]["pitch_post_hra"], stats["2016"]["pitch_post_hra"],
                              stats["2017"]["pitch_post_hra"], stats["2018"]["pitch_post_hra"],
                              stats["2019"]["pitch_post_hra"]]
    graph_regular_vs_post(y_label_pitch_hra_regular, y_label_pitch_hra_post, "Home Run Average", "HRA")
    """


if __name__ == '__main__':
    main()
