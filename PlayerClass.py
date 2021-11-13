# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:34:44 2021

@author: angel
"""
import csv


class Player:
    # this class takes in the name of a player and then gets all the stats on
    # that player, creating a player object that holds all their stats
    # each player has a dict for each stat that has the year as key and
    # value is their stat for that year

    def __init__(self, ID="", First="", Last=""):
        # if id given, get first and last name, if names given then get id
        self.id = ID

        if ID:
            self.get_name(self.id)

        elif First and Last:
            self.name = (First + " " + Last)
            self.get_id(First, Last)

        self.bat_avg = {}
        self.get_bat_avg(self.id)

        self.post_bat_avg = {}
        self.get_post_bat_avg(self.id)

        self.ERA = {}
        self.get_ERA(self.id)

        self.post_ERA = {}
        self.get_post_ERA(self.id)

        self.bat_hr = {}
        self.get_bat_hr(self.id)

        self.post_bat_hr = {}
        self.get_post_bat_hr(self.id)

        self.pitch_hr = {}
        self.get_pitch_hr(self.id)

        self.post_pitch_hr = {}
        self.get_post_pitch_hr = {}

    # Generic Info     
    def get_id(self, First, Last):
        # uses name of player to get their player id from people.csv
        with open("People.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[13] == First and row[14] == Last:  # find row by name
                    self.id = row[0]

    def get_name(self, ID):
        # uses id of player to get their name from people.csv
        with open("People.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.name = (row[13] + " " + row[14])

    def return_id(self):
        ID = self.id
        return ID

    def return_name(self):
        return self.name

    # Batting Stats!!!
    def get_bat_avg(self, ID):
        # uses player id to get at bats and hits for player, then divides
        # them to find batting average, appends that value to bat_avg w/ year
        with open("Batting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID and int(row[6]) != 0:  # get row with player's id
                    avg = int(row[8]) / int(row[6])  # make sure they bat <1
                    self.bat_avg[row[1]] = avg  # divide to get avg

    def return_bat_avg(self, year=""):
        # return the batting average, either all years or specified year
        if year:
            return self.bat_avg[year]
        else:
            return self.bat_avg

    def get_post_bat_avg(self, ID):
        # uses player id to get at bats and hits for player, then divides
        # them to find batting average, appends that value to bat_avg w/ year
        with open("BattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[2] == ID and int(row[6]) != 0:  # get row with player's id
                    avg = int(row[8]) / int(row[6])  # make sure bat <1
                    self.post_bat_avg[row[0]] = avg

    def return_post_bat_avg(self, year=""):
        # return the post batting average, either all years or specified year
        if year:
            return self.post_bat_avg[year]
        else:
            return self.post_bat_avg

    def get_bat_hr(self, ID):
        # uses player id to get batter's hr number
        with open("Batting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row == ID:
                    self.bat_hr[row[1]] = row[11]

    def return_bat_hr(self, year=""):
        # return the batter's hrs, either all years or specified year
        if year:
            return self.bat_hr[year]
        else:
            return self.bat_hr

    def get_post_bat_hr(self, ID):
        # uses player id to get batter's post hr number
        with open("BattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row == ID:
                    self.post_bat_hr[row[0]] = row[11]

    def return_post_bat_hr(self, year=""):
        # return the batter's hrs post season, either all years or specified year
        if year:
            return self.post_bat_hr[year]
        else:
            return self.post_bat_hr

    # Pitching stats!!!
    def get_ERA(self, ID):
        # uses player ID to get their ERA
        with open("Pitching.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.ERA[row[1]] = row[19]

    def return_ERA(self, year=""):
        # return player's ERA, either all years or specified year
        if year:
            return self.ERA[year]
        else:
            return self.ERA

    def get_post_ERA(self, ID):
        # uses player ID to get their ERA
        with open("PitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.post_ERA[row[1]] = row[19]

    def return_post_ERA(self, year=""):
        # return player's ERA, either all years or specified year
        if year:
            return self.post_ERA[year]
        else:
            return self.post_ERA

    def get_pitch_hr(self, ID):
        # uses player ID to get the amount of hrs they pitched
        with open("Pitching.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.pitch_hr[row[1]] = row[15]

    def return_pitch_hr(self, year=""):
        # return amount of hrs player pitched, either all years or specified year
        if year:
            return self.pitch_hr[year]
        else:
            return self.pitch_hr

    def get_post_pitch_hr(self, ID):
        # uses player ID to get the amount of hrs they pitched post season
        with open("PitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.pitch_hr[row[1]] = row[15]

    def return_post_pitch_hr(self, year=""):
        # return amount of hrs player pitched post, either all years or specified year
        if year:
            return self.post_pitch_hr[year]
        else:
            return self.post_pitch_hr

            # add homeruns from batter and homeruns from pitcher pre and post

    # How to print   
    def __repr__(self):
        return self.name
