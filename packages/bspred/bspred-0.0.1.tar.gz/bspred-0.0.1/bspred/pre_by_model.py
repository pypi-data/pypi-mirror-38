#Generates raw predictions of departures and arrivals.

import pandas as pd
import numpy as np
from keras.models import load_model
from .get_path import *


def rescale_input(array_of_nbhd_p):
    new_array = []
    l = len(array_of_nbhd_p)
    path = get_path()
    df = pd.read_csv(path+'scale.csv', sep = ',', engine='python')
    average = df['average'].values
    std = df['std'].values
    for i in range(l):
        profile = array_of_nbhd_p[i]
        profile = np.asarray(profile)
        new_profile = (profile-average)/std
        new_array.append(new_profile)
    return new_array

def rescale_output(Arrivals_raw, Departures_raw):
    l = len(Arrivals_raw)
    path = get_path()
    df = pd.read_csv(path+'output_scale.csv', sep = ',', engine='python')
    Arrivals_average = df.loc[0]['average']
    Arrivals_std = df.loc[0]['std']
    Departures_average = df.loc[1]['average']
    Departures_std = df.loc[1]['std']
    Arrivals = Arrivals_raw*Arrivals_std+Arrivals_average
    Departures = Departures_raw*Departures_std+Departures_average
    return Arrivals, Departures

def pre_simple(Nbhd_profile):
    Nbhd_p = rescale_input(Nbhd_profile)
    Departures_raw = []
    Arrivals_raw = []
    path = get_path()
    Departures_model = load_model(path+'Departures_model.h5')
    Arrivals_model = load_model(path+'Arrivals_model.h5')
    for i in Nbhd_p:
        a = Arrivals_model.predict(np.array([i,]))[0][0]
        d = Departures_model.predict(np.array([i,]))[0][0]
        Arrivals_raw.append(a)
        Departures_raw.append(d)
    Arrivals_raw = np.asarray(Arrivals_raw)
    Departures_raw = np.asarray(Departures_raw)
    Arrivals, Departures = rescale_output(Arrivals_raw, Departures_raw)
    return Arrivals, Departures



