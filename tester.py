# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 20:39:41 2021

@author: angel
"""
from PlayerClass import Player
from TeamClass import Team


# this is where i'm testing some code
def main():
    """
    Can create player object using either first/last name or player ID
    Then can get any of the following stats from player. You can also
    specify the year for any stat you want.
    """
    player = Player("altuvjo01")
    print(player)
    print("Bat avg", player.return_bat_avg())
    print("Post bat avg", player.return_post_bat_avg())
    print("ERA", player.return_ERA())
    print("Post ERA", player.return_post_ERA())
    print("Batting HRs", player.return_bat_hr())
    print("Post batting HRs", player.return_post_bat_hr())
    print("Pitching HRs", player.return_pitch_hr())
    print("Post pitching HRs", player.return_post_pitch_hr())

    '''
    To create a team object, give the year and team code. It will create 
    a dictionary containing player objects for all the players in that team 
    that year. You can then call specific team stats or individual player 
    stats from the team. Each player object will still have stats for all years,
    so still must specify what year you want stats for when calling player
    objects from team object.
    
    Team codes:
        Red Sox -> BOS
        Yankees -> NYA
        Astros -> HOU
        Dodgers -> LAN
    '''
'''
    team = Team("BOS", "2015")
    print("Players:", team)
    print("Win percentage:", team.return_wins())
    print("Rank:", team.return_rank())
    print("Team Size:", team.size())
'''

if __name__ == '__main__':
    main()
