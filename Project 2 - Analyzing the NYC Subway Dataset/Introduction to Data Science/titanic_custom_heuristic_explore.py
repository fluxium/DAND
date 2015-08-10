import pandas as pd
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:41:58 2015

@author: mahlo_000
"""

df = pd.read_csv('C:/Users/mahlo_000/Desktop/Add to Source Control/titanic_data.csv')
df = df.fillna(df.mean()['Age':'Age'])

dfSurvived = df.groupby('Survived')
dfSurvived.describe()
dfNSurvived = df[df['Survived'] == 0]
dfNSurvived.describe()

dfFSurvived = dfSurvived[dfSurvived['Sex'] == 'female']
dfFNSurvived = dfNSurvived[dfNSurvived['Sex'] == 'female']

