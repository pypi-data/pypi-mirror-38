#Please make sure that the input is a pandas dataframe containing information of the coordinates. The output will also be a dataframe.

import pandas as pd
import numpy as np
import os
import sys

from .bs_matrix import *
from .nbhd_p import *
from .pre_by_model import *
from .get_path import *

def confidence_interval(Arrivals, Departures,std = 0.019657):
    l = len(Arrivals)
    r = 1.96 * std
    lw = 1-r
    up = 1+r
    Arrivals_CI = []
    Departures_CI = []
    for i in range(l):
        a = Arrivals[i]
        d = Departures[i]
        a_CI = [a*lw, a*up]
        d_CI = [d*lw, d*up]
        Arrivals_CI.append(a_CI)
        Departures_CI.append(d_CI)
    return Arrivals_CI, Departures_CI


def predict(df_raw):
    df = df_raw[['latitude','longitude']]
    df = df.dropna(how='any')
    Nbhd_profile = get_profile(df)
    Arrivals, Departures = pre_simple(Nbhd_profile)
    if len(Arrivals)>1:
        matrix = get_matrix(df)
        inverse = np.linalg.inv(matrix)
        Departures_corrected = inverse.dot(Departures)
        Arrivals_corrected = inverse.dot(Arrivals)
        df['Arrivals'] = Arrivals_corrected
        df['Departures'] = Departures_corrected
        Arrivals_CI, Departures_CI = confidence_interval(Arrivals_corrected, Departures_corrected)
    else:
        df['Arrivals'] = Arrivals
        df['Departures'] = Departures
        Arrivals_CI, Departures_CI = confidence_interval(Arrivals, Departures)
    df['Arrivals_CI'] = Arrivals_CI
    df['Departures_CI'] = Departures_CI
    return df

def update_by_rm(df_old, remove_list):
    df_old = df_old[['station id','latitude','longitude','Arrivals','Departures','name']]
    names = df_old['name']
    for name in remove_list:
        if name in names:
            df_old = df_old[df_old['name']!=name]
    return df_old




def predict_with_Citibike(df_raw, remove_list=None):
    df_new = df_raw[['latitude','longitude']]
    df_new = df_new.dropna(how='any')
    if len(df_new)>0:
        Nbhd_profile = get_profile(df_new)
        Arrivals, Departures = pre_simple(Nbhd_profile)
        df_new['Arrivals'] = Arrivals
        df_new['Departures'] = Departures
    else:
        df_new['Arrivals'] = np.nan
        df_new['Arrivals'] = np.nan
    df_new['station id'] = np.nan
    df_new['name'] = np.nan
    df_new = df_new[['station id','latitude','longitude','Arrivals','Departures','name']]
    path = get_path()
    df_old = pd.read_csv(path + 'stations_reshaped.csv', sep = ',', engine='python')
    if remove_list:
        df_old_updated = update_by_rm(df_old, remove_list)
    else:
        df_old_updated = df_old[['station id','latitude','longitude','Arrivals','Departures','name']]
    df = df_old_updated.append(df_new)
    df = df.reset_index(drop=True)
    Arrivals_total = df['Arrivals'].values
    Departures_total = df['Departures'].values
    df = df.drop(['Arrivals','Departures'], axis=1)
    matrix = get_matrix(df)
    inverse = np.linalg.inv(matrix)
    Departures_corrected = inverse.dot(Departures_total)
    Arrivals_corrected = inverse.dot(Arrivals_total)
    df['Arrivals'] = Arrivals_corrected
    df['Departures'] = Departures_corrected
    Arrivals_CI, Departures_CI = confidence_interval(Arrivals_corrected, Departures_corrected)
    df['Arrivals_CI'] = Arrivals_CI
    df['Departures_CI'] = Departures_CI
    return df













