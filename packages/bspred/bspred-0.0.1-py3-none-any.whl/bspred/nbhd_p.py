#Generates the neighborhood profiles for the given coordinates.

import pandas as pd
import numpy as np
import os
from .get_path import *

def get_dfs():
    path = get_path()
    city_data_path = path + 'city_data/'

    dfs = {}
    for root, dirs, files in os.walk(city_data_path):
        for file in files:
            if 'csv' in file:
                filename = os.path.splitext(file)[0]
                dfs[filename] = pd.read_csv(city_data_path+file, engine='python')
    return dfs

def distance(c_1,c_2):
    x = (c_1[0] - c_2[0])**2
    y = (c_1[1] - c_2[1])**2
    return (x+y)**0.5

def select_from_df(coordinates, df, delta):
    lat = coordinates[0]
    lon = coordinates[1]
    new_df = pd.DataFrame()
    new_df = df.loc[(df['latitude'] > lat-delta) & (df['latitude'] < lat+delta)]
    new_df = new_df.loc[(new_df['longitude'] > lon-delta) & (new_df['longitude'] < lon+delta)]
    new_df = new_df.reset_index(drop=True)
    return new_df

def general_profile(coordinates, df, unit, whole_range):
    delta=unit*whole_range
    profile = list(0 for i in range(whole_range))
    new_df = select_from_df(coordinates, df, delta)
    l = len(new_df)
    for i in range(l):
        target = [new_df.loc[i]['latitude'],new_df.loc[i]['longitude']]
        d = distance(coordinates, target)
        index = int(round(d/unit)-1)
        if index == -1:
            index = 0
        if index < whole_range:
            profile[index] += 1
    return profile


def get_neighborhood_profile(coordinates, neighborhood, unit=0.001, whole_range=50):
    profile = []
    names = ['Business', 'Property', 'MTA', 'Buses', 'Violation', 'Misdemeanor', 'Felony']
    for i in names:
        profile += general_profile(coordinates, neighborhood[i], unit, whole_range)
    return profile

def get_profile(df):
    l = len(df)
    Nbhd_profile = []
    neighborhood =  get_dfs()
    for i in range(l):
        temporary = df.loc[i]
        coordinates = [temporary['latitude'], temporary['longitude']]
        Nbhd_profile.append(get_neighborhood_profile(coordinates, neighborhood))
    return Nbhd_profile


