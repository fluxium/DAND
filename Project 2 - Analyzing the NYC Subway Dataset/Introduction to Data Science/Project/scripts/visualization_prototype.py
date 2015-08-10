import matplotlib.pyplot as plt
from ggplot import *
import numpy as np
import pandas as pd

def plot_weather_data(turnstile_weather):
    ''' 
    plot_weather_data is passed a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.
    
    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning 
    ridership and time of day in exercise #1, maybe look at weather and try to make a 
    histogram in this exercise). Or try to use multiple encodings in your graph if 
    you didn't in the previous exercise.
    
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out the link 
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather 
    dataframe.
     
   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    turnstile_weather.is_copy = False
    #turnstile_weather['xgress'] = turnstile_weather['ENTRIESn_hourly'] - turnstile_weather['EXITSn_hourly']
    #turnstile_weather['xgress'] = turnstile_weather['xgress'] / (turnstile_weather['ENTRIESn_hourly'].count() + turnstile_weather['EXITSn_hourly'].count())
    
    turnstile_weather['DATEn'] = pd.to_datetime(turnstile_weather['DATEn'])
    turnstile_weather = turnstile_weather.set_index(turnstile_weather['DATEn'])
    
    turnstile_weather['DOW'] = turnstile_weather.index.weekday
    #print type(turnstile_weather.index)

    dowGroups = turnstile_weather.groupby(['DOW']).mean()
    dowGroups.index.name = 'DOW'
    dowGroups = dowGroups.reset_index()
    
    plot = ggplot(dowGroups, aes(x='DOW', y='ENTRIESn_hourly')) + geom_line()
    plot += geom_point()
    plot += ylab('Mean ENTRIESn_hourly')
    plot += xlab('Day of the Week')
    plot += ggtitle('Mean Hourly Entries by Day of the Week')
    return plot

turnstileData = pd.read_csv('../datasets/turnstile_data_master_with_weather.csv')
p = plot_weather_data(turnstileData)
print(p)