# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 22:08:54 2021

@author: angel
"""
from PlayerClass import Player
import csv

class Team:
    # this class takes team id and year and builds a roster full of
    # player objects of players who were in that team that year
    # players are in a dict, with key being their id and value their object
    # also gets some team stats for that year
    
    def __init__(self, ID, year):
        self.id = ID
        self.year = year
        
        self.players = {}
        self.get_players(self.id, self.year)
        print(self.players)
        
    
    def get_players(self, ID, year):
        # goes through Appearances file, creates player object for any player
        # that is in the team that year and adds object to players dict
        with open("Appearances.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == year and row[1] == ID:
                    self.players[row[3]] = Player(row[3])
            
    def __repr__(self):
        roster = []
        for key, value in self.players.items():
            roster.append(value)
        return "p"
    

                    