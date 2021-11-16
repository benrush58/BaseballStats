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
        self.get_players()

        self.wins = ""
        self.get_wins()

        self.rank = ""
        self.get_rank()

    def get_players(self):
        # goes through Appearances file, creates player object for any player
        # that is in the team that year and adds object to players dict
        with open("FilteredAppearances.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[2] == self.id:
                    self.players[row[4]] = Player(row[4])

    def size(self):
        # returns size of team
        return len(self.players)

    def get_wins(self):
        # goes through team file, finds amount of wins and losses
        # for the year, and gets win percentage
        with open("FilteredTeams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    wins = int(row[9])
                    losses = int(row[10])
                    self.wins = wins / (wins + losses)

    def return_wins(self):
        # returns win percentage
        return self.wins

    def get_rank(self):
        # goes through the team file and gets team rank
        with open("FilteredTeams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    self.rank = row[6]

    def return_rank(self):
        # returns team's rank at end of season
        return self.rank

    def reg_ba(self):
        ba_sum = 0
        num_ba = 0
        for player in list(self.players.values()):
            ba = player.return_bat_avg()
            if self.year in ba.keys():
                num_ba += 1
                ba_sum += float(ba[self.year])
        if num_ba != 0:
            return ba_sum / num_ba
        else:
            return 'No player BAs found'

    def post_ba(self):
        ba_sum = 0
        num_ba = 0
        for player in list(self.players.values()):
            ba = player.return_post_bat_avg()
            if self.year in ba.keys():
                num_ba += 1
                ba_sum += float(ba[self.year])
        if num_ba != 0:
            return ba_sum / num_ba
        else:
            return 'No player BAs found'

    def reg_era(self):
        with open('FilteredTeams.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    return row[29]

    def post_era(self):
        era_sum = 0
        num_era = 0
        for player in list(self.players.values()):
            era = player.return_post_ERA()
            if self.year in era.keys():
                num_era += 1
                era_sum += float(era[self.year])
        if num_era != 0:
            return era_sum / num_era
        else:
            return 'No player ERAs found'

    def reg_hra(self):
        with open('FilteredTeams.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    return int(row[20]) / int(row[16])

    def post_hra(self):
        hra_sum = 0
        num_rows = 0
        for id, player in list(self.players.items()):
            with open('FilteredBattingPost.csv') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[1] == self.year and row[3] == id and int(row[7]) != 0:
                        hra_sum += int(row[12]) / int(row[7])
                        num_rows += 1
        if num_rows != 0:
            return hra_sum / num_rows
        else:
            return 'No player HRs found'

    def __repr__(self):
        # when the object is printed, it gives a string of the 
        # names of all the player objects in team
        roster = ""
        for key, value in self.players.items():
            name = value.return_name()
            roster += name + ", "
        return roster
