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
        
        self.wins = ""
        self.get_wins()
        
        self.rank = ""
        self.get_rank()        
        
    
    def get_players(self, ID, year):
        # goes through Appearances file, creates player object for any player
        # that is in the team that year and adds object to players dict
        with open("Appearances.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == self.year and row[1] == self.id:
                    self.players[row[3]] = Player(row[3])
    
    
    def size(self):
        # returns size of team
        return len(self.players)
    
    def get_wins(self):
        # goes through team file, finds amount of wins and losses
        # for the year, and gets win percentage
        with open("Teams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == self.year and row[2] == self.id:
                    wins = int(row[8])
                    losses = int(row[9])
                    self.wins = wins / (wins + losses)

    def return_wins(self):
        # returns win percentage
        return self.wins  

    def get_rank(self):
        #goes through the team file and gets team rank
         with open("Teams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == self.year and row[2] == self.id:
                    self.rank = row[5]
                    
    def return_rank(self):
        # returns team's rank at end of season
        return self.rank
        
            
    def __repr__(self):
        # when the object is printed, it gives a string of the 
        # names of all the player objects in team
        roster = ""
        for key, value in self.players.items():
            name = value.return_name()
            roster += name + ", "
        return roster


    

                    