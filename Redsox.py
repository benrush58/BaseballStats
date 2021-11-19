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
        print(team)
        #reg_batavg = team.reg_ba()
        #post_batavg = team.post_ba()
        #reg_era = team.reg_era()
        #post_era = team.post_era()
        #reg_hra = team.reg_hra()
        #post_hra= team.post_hra()
        #pitch_reg_hra = team.pitch_reg_hra()
        #pitch_post_hra = team.pitch_post_hra()

        years[team.year] = {"reg_batavg": team.reg_ba(), "post_batavg": team.post_ba(), "reg_era": team.reg_era(),
                            "post_era": team.post_era(), "reg_hra": team.reg_hra(), "post_hra": team.post_hra(),
                            "pitch_reg_hra": team.pitch_reg_hra(), "pitch_post_hra": team.pitch_post_hra()}




def main():
    # No playoff appearance (78-84, not good, last in AL East)
    redsox15 = Team('BOS', 2015)
    # Eliminated in first round (93-69, first in AL East, 3rd in AL, projected to lose in the first round)
    redsox16 = Team('BOS', 2016)
    # Eliminated in first round (93-69 again, first in AL East, 3rd in AL, projected to lose in the first round
    redsox17 = Team('BOS', 2017)
    # Won world series (108-54, first  in AL East, 1st in all of baseball, projected to win the world series
    redsox18 = Team('BOS', 2018)
    # Not close to playoffs, could be interesting to examine the fall off
    redsox19 = Team('BOS', 2019)
    teams = [redsox15, redsox16, redsox17, redsox18, redsox19]
    stats = get_team_stats(teams)
    print(stats)


if __name__ == '__main__':
    main()