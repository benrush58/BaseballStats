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
        self.get_post_pitch_hr(self.id)

        self.post_pitch_innings = {}
        self.get_innings_pitched_post(self.id)

        self.post_earned_runs = {}
        self.get_earned_runs_post(self.id)

        self.plate_appearances = {}
        self.get_plate_appearances(self.id)

        self.hits = {}
        self.get_hits(self.id)

        self.plate_appearances_post = {}
        self.get_plate_appearances_post(self.id)

        self.hits_post = {}
        self.get_hits_post(self.id)

    # Generic Info     
    def get_id(self, First, Last):
        """
        name: get_id
        paramater: self(a Player)
        returns: none, gets player's ID
        """
        with open("People.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[13] == First and row[14] == Last:  # find row by name
                    self.id = row[0]

    def get_name(self, ID):
        """
        name: get_name
        paramater: self, a Player
        returns: none, gets player's name
        """
        # uses id of player to get their name from people.csv
        with open("People.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == ID:
                    self.name = (row[13] + " " + row[14])

    def return_id(self):
        """
        name: return_id
        paramater: self, a Player
        returns: id, player value
        """
        ID = self.id
        return ID

    def return_name(self):
        """
        name: return_name
        paramater: self, a Player
        returns: name, player name
        """
        return self.name

    # Batting Stats!!!
    def get_bat_avg(self, ID):
        """
        name: get_bat_avg
        paramater: self, a Player
        returns: none, gets player's batting average
        """
        with open("FilteredBatting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID and int(row[7]) != 0:  # get row with player's id
                    avg = int(row[9]) / int(row[7])  # make sure they bat <1
                    if row[2] in self.bat_avg:
                        self.bat_avg[row[2]].append(avg)  # divide to get avg
                    else:
                        self.bat_avg[row[2]] = [avg]
            for year, avg in self.bat_avg.items():
                self.bat_avg[year] = sum(avg) / len(avg)

    def return_bat_avg(self, year=""):
        """
        name: return_bat_avg
        paramater: self(a Player) and an optional year
        returns: player's batting average, player value
        """
        if year:
            return self.bat_avg[year]
        else:
            return self.bat_avg

    def get_plate_appearances(self, ID):
        """
        name: get_plate_appearances
        paramater: self, a Player
        returns: none, gets player's plate appearances
        """
        with open("FilteredBatting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID and int(row[7]) != 0:  # get row with player's id
                    avg = int(row[9]) / int(row[7])  # make sure they bat <1
                    if row[2] in self.plate_appearances:
                        value = int(self.plate_appearances[row[2]])
                        newer = value + int(row[7])
                        self.plate_appearances[row[2]] = newer
                    else:
                        self.plate_appearances[row[2]] = int(row[7])

    def return_plate_appearances(self, year=""):
        """
        name: return_plate_appearances
        paramater: self(a Player) and an optional year
        returns: player's plate appearances
        """
        if year:
            if len(self.plate_appearances) != 0:
                try:
                    pa = self.plate_appearances[year]
                    return pa
                except:
                    return 0
            else:
                return 0
        else:
            return self.plate_appearances

    def get_hits(self, ID):
        """
        name: get_hits
        paramater: self, a Player
        returns: none, gets player's hits
        """
        with open("FilteredBatting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID and int(row[7]) != 0:  # get row with player's id
                    avg = int(row[9]) / int(row[7])  # make sure they bat <1
                    if row[2] in self.hits:
                        value = int(self.hits[row[2]])
                        newer = value + int(row[9])
                        self.hits[row[2]] = newer
                    else:
                        self.hits[row[2]] = int(row[9])

    def return_hits(self, year=""):
        """
        name: return_hits
        paramater: self(a Player) and an optional year
        returns: player's hits
        """
        if year:
            if len(self.hits) != 0:
                try:
                    hit = self.hits[year]
                    return hit
                except:
                    return 0
            else:
                return 0
        else:
            return self.hits

    def get_post_bat_avg(self, ID):
        """
        name: get_post_bat_avg
        paramater: self, a Player
        returns: none, gets player's post season batting average
        """
        with open("FilteredBattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[3] == ID and int(row[7]) != 0:  # get row with player's id
                    avg = int(row[9]) / int(row[7])  # make sure bat <1
                    if row[1] in self.post_bat_avg:
                        self.post_bat_avg[row[1]].append(avg)
                    else:
                        self.post_bat_avg[row[1]] = [avg]
            for year, avg in self.post_bat_avg.items():
                self.post_bat_avg[year] = sum(avg) / len(avg)

    def return_post_bat_avg(self, year=""):
        """
        name: return_post_bat_avg
        paramater: self(a Player) and an optional year
        returns: player's post season batting average
        """
        # return the post batting average, either all years or specified year
        if year:
            return self.post_bat_avg[year]
        else:
            return self.post_bat_avg

    def get_plate_appearances_post(self, ID):
        """
        name: get_plate_appearances_post
        paramater: self, a Player
        returns: none, gets player's post season plate appearances
        """
        with open("FilteredBattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[3] == ID and int(row[7]) != 0:  # get row with player's id
                    avg = int(row[9]) / int(row[7])  # make sure they bat <1
                    if row[1] in self.plate_appearances_post:
                        value = int(self.plate_appearances_post[row[1]])
                        newer = value + int(row[7])
                        self.plate_appearances_post[row[1]] = newer
                    else:
                        self.plate_appearances_post[row[1]] = int(row[7])

    def return_plate_appearances_post(self, year=""):
        """
        name: return_plate_appearances_post
        paramater: self(a Player) and an optional year
        returns: player's post season plate appearances
        """
        if year:
            if len(self.plate_appearances_post) != 0:
                try:
                    pa = self.plate_appearances_post[year]
                    return pa
                except:
                    return 0
            else:
                return 0
        else:
            return self.plate_appearances_post

    def get_hits_post(self, ID):
        """
         name: get_hits_post
         paramater: self, a Player
         returns: none, gets player's post season hits
         """
        with open("FilteredBattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[3] == ID and int(row[7]) != 0:  # get row with player's id
                    # avg = int(row[9]) / int(row[7])  # make sure they bat <1
                    if row[1] in self.hits_post:
                        value = int(self.hits_post[row[1]])
                        newer = value + int(row[9])
                        self.hits_post[row[1]] = newer
                    else:
                        self.hits_post[row[1]] = int(row[9])

    def return_hits_post(self, year=""):
        """
        name: return_hits_post
        paramater: self(a Player) and an optional year
        returns: player's post season hits
        """
        if year:
            if len(self.hits_post) != 0:
                try:
                    hit = self.hits_post[year]
                    return hit
                except:
                    return 0
            else:
                return 0
        else:
            return self.hits_post

    def get_bat_hr(self, ID):
        """
         name: get_bat_hr
         paramater: self, a Player
         returns: none, gets player's home run total
         """
        with open("FilteredBatting.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.bat_hr:
                        self.bat_hr[row[2]] += float(row[12])
                    else:
                        self.bat_hr[row[2]] = float(row[12])

    def return_bat_hr(self, year=""):
        """
        name: return_bat_hr
        paramater: self(a Player) and an optional year
        returns: player's home run total
        """
        if year:
            return self.bat_hr[year]
        else:
            return self.bat_hr

    def get_post_bat_hr(self, ID):
        """
         name: get_post_bat_hr
         paramater: self, a Player
         returns: none, gets player's post season home run total
         """
        with open("FilteredBattingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[3] == ID:
                    if row[1] in self.post_bat_hr:
                        self.post_bat_hr[row[1]] += float(row[12])
                    else:
                        self.post_bat_hr[row[1]] = float(row[12])

    def return_post_bat_hr(self, year=""):
        """
        name: return_post_bat_hr
        paramater: self(a Player) and an optional year
        returns: player's post season home run total
        """
        if year:
            return self.post_bat_hr[year]
        else:
            return self.post_bat_hr

    # Pitching stats!!!
    def get_ERA(self, ID):
        """
         name: get_ERA
         paramater: self, a Player
         returns: none, gets player's post season plate appearances
         """
        with open("FilteredPitching.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.ERA:
                        self.ERA[row[2]].append(float(row[20]))
                    else:
                        self.ERA[row[2]] = [float(row[20])]
            for year, era in self.ERA.items():
                self.ERA[year] = sum(era) / len(era)

    def return_ERA(self, year=""):
        """
        name: return_ERA
        paramater: self(a Player) and an optional year
        returns: player's ERA
        """
        # return player's ERA, either all years or specified year
        if year:
            return self.ERA[year]
        else:
            return self.ERA

    def get_post_ERA(self, ID):
        """
         name: get_post_ERA
         paramater: self, a Player
         returns: none, gets player's post season ERA
         """
        with open("FilteredPitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID and row[20] != 'inf':
                    if row[2] in self.post_ERA:
                        self.post_ERA[row[2]].append(float(row[20]))
                    else:
                        self.post_ERA[row[2]] = [float(row[20])]
            for year, era in self.post_ERA.items():
                self.post_ERA[year] = sum(era) / len(era)

    def return_post_ERA(self, year=""):
        """
        name: return_post_ERA
        paramater: self(a Player) and an optional year
        returns: player's post season hits
        """
        if year:
            return self.post_ERA[year]
        else:
            return self.post_ERA

    def get_innings_pitched_post(self, ID):
        """
         name: get_innings_pitched_post
         paramater: self, a Player
         returns: none, gets player's post season innings pitched
         """
        with open("FilteredPitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.post_pitch_innings:
                        val = self.post_pitch_innings[row[2]]
                        new = val + (float(row[13]) / 3.0)
                        self.post_pitch_innings[row[2]] = new
                    else:
                        self.post_pitch_innings[row[2]] = (float(row[13]) / 3.0)

    def return_innings_pitched_post(self, year=""):
        """
        name: return_innings_pitched_post
        paramater: self(a Player) and an optional year
        returns: player's post season innings pitched
        """
        if year:
            if len(self.post_pitch_innings) != 0:
                try:
                    inn = self.post_pitch_innings[year]
                    return inn
                except:
                    return 0
            else:
                return 0
        else:
            return self.post_pitch_innings

    def get_earned_runs_post(self, ID):
        """
         name: get_earned_runs_post
         paramater: self, a Player
         returns: none, gets player's post season earned runs
         """
        with open("FilteredPitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.post_earned_runs:
                        value = float(self.post_earned_runs[row[2]])
                        newer = value + float(row[15])
                        self.post_earned_runs[row[2]] = newer
                    else:
                        self.post_earned_runs[row[2]] = row[15]

    def return_earned_runs_post(self, year=""):
        """
        name: return_earned_runs_post
        paramater: self(a Player) and an optional year
        returns: player's post season earned runs
        """
        if year:
            if len(self.post_earned_runs) != 0:
                try:
                    inn = self.post_earned_runs[year]
                    # print(self.name, self.post_earned_runs)
                    return inn
                except:
                    return 0
            else:
                return 0
        else:
            return self.post_earned_runs

    def get_pitch_hr(self, ID):
        """
         name: get_pitch_hr
         paramater: self, a Player
         returns: none, gets player's post season home runs allowed
         """
        with open("FilteredPitching.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.pitch_hr:
                        self.pitch_hr[row[2]] += int(row[16])
                    else:
                        self.pitch_hr[row[2]] = int(row[16])

    def return_pitch_hr(self, year=""):
        """
        name: return_pitch_hr
        paramater: self(a Player) and an optional year
        returns: player's home runs allowed
        """
        if year:
            return self.pitch_hr[year]
        else:
            return self.pitch_hr

    def get_post_pitch_hr(self, ID):
        """
         name: get_post_pitch_hr
         paramater: self, a Player
         returns: none, gets player's post season home runs allowed
         """
        with open("FilteredPitchingPost.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1] == ID:
                    if row[2] in self.post_pitch_hr:
                        self.post_pitch_hr[row[2]] += int(row[16])
                    else:
                        self.post_pitch_hr[row[2]] = int(row[16])

    def return_post_pitch_hr(self, year=""):
        """
        name: return_post_pitch_hr
        paramater: self(a Player) and an optional year
        returns: player's post season home runs allowed
        """
        if year:
            return self.post_pitch_hr[year]
        else:
            return self.post_pitch_hr

    # How to print   
    def __repr__(self):
        return self.name
