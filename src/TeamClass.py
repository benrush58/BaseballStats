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
        """
        name: get_players
        paramater: self(a Team)
        returns: none, gets players of that team
        """
        """goes through Appearances file, creates player object for any player
        that is in the team that year and adds object to players dict"""
        with open("data_csv/FilteredAppearances.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[2] == self.id:
                    self.players[row[4]] = Player(row[4])

    def size(self):
        """
        name: size
        paramater: self(a Team)
        returns: number of players on the team
        """
        return len(self.players)

    def get_wins(self):
        """
        name: get_wins
        paramater: self(a Team)
        returns: none, gets win percentage of Teeam
        """
        with open("data_csv/FilteredTeams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    wins = int(row[9])
                    losses = int(row[10])
                    self.wins = wins / (wins + losses)

    def return_wins(self):
        """
        name: return_wins
        paramater: self(a Team)
        returns: Team's wins
        """
        return self.wins

    def get_rank(self):
        """
        name: get_rank
        paramater: self(a Team)
        returns: none, gets rank of team
        """
        with open("data_csv/FilteredTeams.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    self.rank = row[6]

    def return_rank(self):
        """
        name: return_rank
        paramater: self(a Team)
        returns: Team's rank at the end of that season
        """
        return self.rank

    def reg_ba(self):
        """
        name: return_ba
        paramater: self(a Team)
        returns: Team's batting average
        """
        hits = 0
        pa = 0
        for player in list(self.players.values()):
            h = player.return_hits(self.year)
            plate = player.return_plate_appearances(self.year)
            hits = hits + h
            pa = pa + plate
        if pa != 0:
            return hits / pa
        else:
            return 'No player BAs found'

    def post_ba(self):
        """
        name: post_ba
        paramater: self(a Team)
        returns: Team's post season batting average
        """
        hits = 0
        pa = 0
        for player in list(self.players.values()):
            h = player.return_hits_post(self.year)
            plate = player.return_plate_appearances_post(self.year)
            hits = hits + h
            pa = pa + plate
        if pa != 0:
            return hits / pa
        else:
            return 'No player BAs found'

    def reg_era(self):
        """
        name: reg_era
        paramater: self(a Team)
        returns: Team's ERA
        """
        with open('data_csv/FilteredTeams.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    return row[29]


    def post_era(self):
        """
        name: post_era
        paramater: self(a Team)
        returns: Team's post season ERA
        """
        earned_runs = 0
        innings_pitched = 0
        for player in list(self.players.values()):
            er = float(player.return_earned_runs_post(self.year))
            ip = float(player.return_innings_pitched_post(self.year))
            earned_runs += er
            innings_pitched += ip
        if innings_pitched != 0:
            # print("Earned runs:", earned_runs)
            # print("Innings pitched:", innings_pitched)
            return (9 * earned_runs) / innings_pitched
        else:
            return 'No player ERAs found'

    def reg_hra(self):
        """
        name: reg_hra
        paramater: self(a Team)
        returns: Team's season HR average per at bat
        """
        with open('data_csv/FilteredTeams.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    return int(row[20]) / int(row[16])

    def post_hra(self):
        """
        name: post_hra
        paramater: self(a Team)
        returns: Team's post season HR average per at bat
        """
        hra_sum = 0
        num_rows = 0
        for id, player in list(self.players.items()):
            with open('data_csv/FilteredBattingPost.csv') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[1] == self.year and row[3] == id and int(row[7]) != 0:
                        hra_sum += int(row[12]) / int(row[7])
                        num_rows += 1
        if num_rows != 0:
            return hra_sum / num_rows
        else:
            return 'No player HRs found'

    def pitch_reg_hra(self):
        """
        name: pitch_reg_hra
        paramater: self(a Team)
        returns: Team's HR allowed average per inning
        """
        with open('data_csv/FilteredTeams.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == self.year and row[3] == self.id:
                    return int(row[35]) / (int(row[33]) / 3)

    def pitch_post_hra(self):
        """
        name: pitch_post_hra
        paramater: self(a Team)
        returns: Team's post season HR allowed average per inning
        """
        hra_sum = 0
        num_rows = 0
        for id, player in list(self.players.items()):
            with open('data_csv/FilteredPitchingPost.csv') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[2] == self.year and row[1] == id and int(row[13]) != 0:
                        hra_sum += int(row[16]) / (int(row[13]) / 3)
                        num_rows += 1
        if num_rows != 0:
            return hra_sum / num_rows
        else:
            return 'No Pitching HRAs Found'

    def __repr__(self):
        # when the object is printed, it gives a string of the 
        # names of all the player objects in team
        roster = ""
        for key, value in self.players.items():
            name = value.return_name()
            roster += name + ", "
        return roster
