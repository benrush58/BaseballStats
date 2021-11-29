from TeamClass import Team
from PlayerClass import Player
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""Goals of this research
1) Identify how each team was projected to do in the post season given their regular season record
2) Identify how each team actually did in the post season compared to the projection
3) Compare stats and players between regular season and post season with all types of graphs
4) Identify which stats and players were the most influential in their regular vs post season performance

Could be interesting to tell the story of the slow rise and the dramatic fall of the Sox in these 5 years"""


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

        years[team.year] = {"reg_batavg": team.reg_ba(), "post_batavg": team.post_ba(), "reg_era": team.reg_era(),
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

    teams = [redsox15, redsox16, redsox17, redsox18, redsox19]
    stats = get_team_stats(teams)
    #print(redsox15.trying_era())
    #print(redsox16.trying_era())
    #print(redsox17.trying_era())
    #print(redsox18.trying_era())
    #print(redsox19.trying_era())

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


if __name__ == '__main__':
    main()
