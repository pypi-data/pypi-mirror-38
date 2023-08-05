# Prediction of Bike Sharing Usage based on Citibike New York Data in 2018

Please download and open the html files to see the plots. The available plots demonstrate the stations with the highest Departures and Arrivals.

To install, please do:

```bash
pip install bspred
```

## Key Variables
Arrivals: number of trips that end at a station per day. 

Departures: number of trips that start at a station per day. 

Characteristic prediction: prediction of bike sharing usage at a specific location, given that there are no bike stations in a vicinity of the location.

## Dependency
numpy, pandas, keras

## Library Description

This is a python library in progress. 

There are two kinds of prediction available. All predictions come with asymptotica 95% confidence intervals.

```python
import bspred
import numpy as np
import pandas as pd

data = pd.DataFrame({
    'latitude':[40.75058535], 
    'longitude':[-73.99468482]
})
```

1. Prediction of characteristic bike sharing usage. 

Please notice that this is not the true bike sharing usage, but rather an order of magnitude analysis.

```python
bspred.predict(data)
```
The results will be: 

Arrivals = 826.452942, Arrivals_CI = [821.8796256964637, 831.0262580925988]

Departures = 839.163513, Departures_CI = [834.5198609039221, 843.8071654632654]

2. Prediction of bike sharing usage given the current active Citibike stations.

```python
bspred.predict_with_Citibike(data)
```

The result will be a pandas dataframe of the predicted bike sharing usage at current bike stations and the newly added ones.

The last row of the dataframe, which is the prediction of bike sharing usage at the new bike station, will be:

Arrivals = 441.030067, Arrivals_CI = [438.58955342277693, 443.4705813647262]
Departures = 474.2624, Departures_CI = [471.63796142662545, 476.88678244901826]

If removing some current Citibike stations is desired, a list of the station names can be passed as remove_list:

```python
bspred.predict_with_Citibike(data, remove_list = [])
```

The names can be extracted from https://member.citibikenyc.com/map/.

Or, to view the current Citibike trip history data, run:

```python
path = bspred.get_path()
df = pd.read_csv(path + '/stations_reshaped.csv', sep=',', engine='python')
df
```
