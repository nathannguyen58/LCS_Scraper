#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:00:53 2021

@author: nathannguyen
"""

import requests
import pandas as pd
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

#Generate a pandas dataframe based on the type of data you want to see
def getList(listType):
    if (listType == 'player'):
        url = "https://gol.gg/players/list/season-ALL/split-ALL/tournament-LCS%20Summer%202021/"
        
    elif (listType == 'team'):
        url = "https://gol.gg/teams/list/season-ALL/split-ALL/tournament-LCS%20Summer%202021/"
    
    r = requests.get(url, headers = {'User-agent': 'Super Bot Power Level Over 9000'})


    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_ = 'table_list playerslist tablesaw trhover')


    columns = [i.get_text(strip = True) for i in table.find("thead").find_all("th")]

    data = []

    table.find("thead").extract()

    for tr in table.find_all("tr"):
        data.append([td.get_text(strip = True) for td in tr.find_all("td")])


    df = pd.DataFrame(data,  columns = columns)
    
    if (listType == 'player'):
        df1 = df.set_index("Player", drop = False)
    elif (listType == 'team'):
        df1 = df.set_index("Name", drop = False)
    
    return df1


df_player = getList('player')
df_team = getList('team')


#Helper method used to retrieve the correct data frame to avoid generating duplicate data frames
def retrieveList(listType):
    if (listType == 'player'):
        return df_player
    
    elif (listType == 'team'):
        return df_team


#Calculates a performance rating for a specific player based on scoring system breakdown used for the E1 Fantasy platform
def generatePlayerRating(player):
    df = retrieveList('player')
    
    df_mask = df['Player'] == player
    
    filtered_df = df[df_mask]
    
    filtered_df['Games'] = pd.to_numeric(filtered_df['Games'])
    
    df_mask = filtered_df['Games'] >= 15
    
    filtered_df = filtered_df[df_mask]
    
    overallPoints = 0.0
    
    overallPoints += pd.to_numeric(filtered_df['Avg kills'][0]) * 3
    overallPoints += pd.to_numeric(filtered_df['Avg deaths'][0]) * -1
    overallPoints += pd.to_numeric(filtered_df['Avg assists'][0]) * 1.5
    overallPoints += pd.to_numeric(filtered_df['CSM'][0]) * 0.02
    
    return overallPoints
    
    
#Calculates a performance rating for a specific team based on scoring system breakdown used for the E1 Fantasy platform    
def generateTeamRating(team):
    df = retrieveList('team')
    
    df_mask = df['Name'] == team
    
    filtered_df = df[df_mask]
    
    overallPoints = 0.0
    
    overallPoints += pd.to_numeric(filtered_df['Win rate'].str[:-1].astype(float)[0])/100 * 2
    overallPoints += pd.to_numeric(filtered_df['Towers killed'][0])
    overallPoints += pd.to_numeric(filtered_df['FT%'].str[:-1].astype(float)[0])/100
    overallPoints += pd.to_numeric(filtered_df['FB%'].str[:-1].astype(float)[0])/100 * 2
    overallPoints += pd.to_numeric(filtered_df['DRAPG'][0]) * 2
    overallPoints += pd.to_numeric(filtered_df['NASHPG'][0]) * 3
    overallPoints += pd.to_numeric(filtered_df['HERPG'][0]) * 2
    
    return overallPoints
    
    

#Compares two players by their individual performance rating
def comparePlayers(p1, p2):
    print('Overall Score for ' + p1 + ": " + str(generatePlayerRating(p1)))
    print('Overall Score for ' + p2 + ": " + str(generatePlayerRating(p2)))
    
#Compares two teams by their team performance rating
def compareTeams(t1, t2):
    print('Overall Score for ' + t1 + ": " + str(generateTeamRating(t1)))
    print('Overall Score for ' + t2 + ": " + str(generateTeamRating(t2)))


#Takes an input for specific position and outputs the top 5 players with the highest KDA
def highestKDA(role):
    df = retrieveList('player')
    df_mask = df['Position'] == role
    filtered_df = df[df_mask]
    
    sorted = filtered_df.sort_values('KDA', ascending = False).head(5)
    print(sorted['KDA'])
    
#Takes an input for a specific position and outputs the top 5 players based on their win percentage
def highestWinRate(role):
    df = retrieveList('player')
    
    df_mask = df['Position'] == role
    
    filtered_df = df[df_mask]
    
    filtered_df['Games'] = pd.to_numeric(filtered_df['Games'])
    
    df_mask = filtered_df['Games'] >= 15
    
    filtered_df = filtered_df[df_mask]
    
    filtered_df['Win rate'] = filtered_df['Win rate'].str[:-1].astype(float)
    sorted = filtered_df.sort_values('Win rate', ascending = False).head(5)
    print(sorted['Win rate'])
    
#Outputs the top 5 teams based on their K:D ratio
def highestKD():
    df = retrieveList('team')
    
    sorted = df.sort_values('K:D', ascending = False).head(5)
    
    print(sorted['K:D'])







