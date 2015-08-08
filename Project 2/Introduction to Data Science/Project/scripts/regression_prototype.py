import statsmodels.api as sm
import pandas as pd
import numpy as np
import scipy
import scipy.stats
import matplotlib.pyplot as plt
    
'''
Some Original comments removed to save space
Code taken from Problem Set 3 > 5 - Linear Regression
'''

def linear_regression(features, values):
    """
    Original comments removed to save space
    """
    #constant added to produce intercept, only adds a constant is one does not already exitst in the data
    fitFeatures = sm.add_constant(features)
    #print(features.shape)
    #print(fitFeatures.shape)
    model = sm.OLS(values, fitFeatures)
    results = model.fit()
    params = results.params[1:]
    intercept = results.params[0]

    return intercept, params

def predictions(dataframe):
    '''
    Some Original comments removed to save space
    Code taken from Problem Set 3 > 5 - Linear Regression
    Provided by instructor
    '''
    # Select Features (try different features!)
    #thunder is a constant of 0. If used, sm.add_constant(features) will not add a constant
    
    #features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']] #0.45804446474
    
    #along with rain, perhaps temperature and wind influence ridership
    #features = dataframe[['rain', 'precipi', 'Hour', 'maxtempi', 'fog', 'mintempi', 'meanwindspdi']] #0.459203243098
    
    #previous but without 'fog'
    #features = dataframe[['rain', 'precipi', 'Hour', 'maxtempi', 'mintempi', 'meanwindspdi']] #does not converge
    
    #all features except some of the problematic ones like thunder
    #features = dataframe[['Hour', 'maxpressurei', 'maxdewpti', 'mindewpti', 'minpressurei', 'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'mintempi', 'meantempi', 'maxtempi',
    #                    'precipi']] #0.46138754392
    
    #removed 'maxdewpti'
    #features = dataframe[['Hour', 'maxpressurei', 'mindewpti', 'minpressurei', 'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'mintempi', 'meantempi', 'maxtempi',
    #                    'precipi']] #0.461284253482
    
    #removed 'minpressurei'
    #features = dataframe[['Hour', 'maxpressurei', 'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'mintempi', 'meantempi', 'maxtempi',
    #                    'precipi']] #0.461154867037 
    
    #removed 'maxpressurei'
    #features = dataframe[['Hour',  'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'mintempi', 'meantempi', 'maxtempi',
    #                    'precipi']] #0.459937880287
    
    #removed 'mintempi'
    #features = dataframe[['Hour',  'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'meantempi', 'maxtempi',
    #                    'precipi']] #0.459910264248
    
    #removed 'maxtempi'
    #features = dataframe[['Hour',  'meandewpti',
    #                    'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'meantempi', 'precipi']] #0.458760123728 
    
    #removed 'fog'
    #features = dataframe[['Hour',  'meandewpti',
    #                    'meanpressurei',  'rain', 'meanwindspdi', 'meantempi', 'precipi']] #0.458586887501
    
    #removed 'meandewpti'
    #features = dataframe[['Hour', 'meanpressurei',  'rain', 'meanwindspdi', 'meantempi', 'precipi']] #0.458574730675
    
    #removed 'precipi'
    #features = dataframe[['Hour', 'meanpressurei',  'rain', 'meanwindspdi', 'meantempi']] #0.458567612582
   
    #removed 'Hour'
    #features = dataframe[['meanpressurei',  'rain', 'meanwindspdi', 'meantempi']] #0.419352827628
    
    #removed 'meanpressurei'
    #features = dataframe[['rain', 'meanwindspdi', 'meantempi']] #0.419151648005
    
    #removed  'meanwindspdi'
    #features = dataframe[['rain', 'meantempi']] #0.418795853695
    
    #removed 'meantempi'
    #features = dataframe[['rain']] #0.418343611355
    
    #added 'Hour' back
    features = dataframe[['rain', 'Hour']] #0.457561363847
    
    #prepare Day of Week feature
    dataframe['DATEn'] = pd.to_datetime(dataframe['DATEn'])
    dataframeTemp = dataframe.set_index(dataframe['DATEn'])
    dataframe['DOW'] = dataframeTemp.index.weekday
    
    #added 'DOW'
    #features = dataframe[['rain', 'Hour', 'DOW']] #0.462709376092
    
    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Add DOW to features using dummy variables
    dummy_dow = pd.get_dummies(dataframe['DOW'], prefix='dow')
    features = features.join(dummy_dow)
    #0.46988063449

    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values

    # Perform linear regression
    intercept, params = linear_regression(features_array, values_array)
    
    print(intercept)
    print(params)
    
    predictions = intercept + np.dot(features_array, params)
    
    print(predictions)    
    
    return predictions

def plot_residuals(turnstile_weather, predictions):
    '''
    Some Original comments removed to save space
    Code taken from Problem Set 3 > 6 - Plotting Residuals
    '''
    plt.figure()
    
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(range = (-15000,15000), label = 'Residual', bins = 25)
    plt.suptitle('Residual of ENTRIESn_hourly and Predictions', fontsize=16)
    plt.legend()
    plt.xlabel('Residual')
    plt.ylabel('Frequency')
    return plt
    
def compute_r_squared(data, predictions):
    '''
    Some Original comments removed to save space
    Code taken from Problem Set 3 > 7 - Compute R^2
    '''
    numerator = np.sum((data - predictions)**2)
    denom = np.sum((data - np.mean(data))**2)
    r_squared = 1 - (numerator / denom)
    
    return r_squared
    
turnstileData = pd.read_csv('../datasets/turnstile_data_master_with_weather.csv')

predict = predictions(turnstileData)

plot_residuals(turnstileData, predict)

r2 = compute_r_squared(turnstileData['ENTRIESn_hourly'], predict)

print("R^2 Value: ", r2)