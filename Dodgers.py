#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 15:51:29 2021

@author: Marta
"""

"""
dodgers file
"""

from TeamClass import Team
from PlayerClass import Player
import matplotlib.pyplot as plt


if __name__ == "__main__":
    dodgers15 = Team('LAN', '2015')
    dodgers16 = Team('LAN', '2016')
    dodgers17 = Team('LAN', '2017')
    dodgers18 = Team('LAN', '2018')
    dodgers19 = Team('LAN', '2019')

    teams = [dodgers15, dodgers16, dodgers17, dodgers18, dodgers19]

    win_percent = []

    for team in teams:
        win_percent.append(team.return_wins())

    plt.bar([1,2,3,4,5], win_percent)    
    