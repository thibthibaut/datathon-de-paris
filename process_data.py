#!/usr/bin/env python

import json
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def parseRawJson():
    # Create a dataframe to hold the data
    dataframe = pd.DataFrame(columns=['bib', 'firstName', 'lastName', 'gender', 'age', 'finishTime', 'avgSpeed'])

    count = 0
    with open('./marathon_data_sanitized.json') as raw_file:
        json_data = json.load(raw_file)
        for chunk in json_data['data']:
            for competitor in chunk['items']:
                count += 1
                print('\r {}'.format(count), end='')
                result = competitor['finalResult']
                person = competitor['person']
                avg_speed = result['averageSpeed']
                finish_time_raw = re.search('(\d\d:\d\d:\d\d)', result['finishTime'])
                time = finish_time_raw.group(0)
                hour = 2 + int(time.split(':')[0])
                minutes = hour*60 + int(time.split(':')[1])
                seconds = minutes*60 + int(time.split(':')[2])
                avg_speed = result['averageSpeed']
                dataframe = dataframe.append(
                        {'bib': competitor['bib'],
                         'firstName': person['firstName'],
                         'lastName': person['lastName'],
                         'gender': person['gender'],
                         'age': person['age'],
                         'finishTime': seconds,
                         'avgSpeed': avg_speed
                         }, ignore_index=True)
    dataframe.to_pickle('./dataframe.pickle')
    dataframe.to_csv('./marathon-paris-2019.csv')
    return dataframe
            

if __name__ == '__main__':
    df = None
    try:
        df = pd.read_pickle('./dataframe.pickle')
    except:
        df = parseRawJson()

    nbr_participants = len(df)
    nbr_participants_M = len(df[df.gender =='M'])
    nbr_participants_F = len(df[df.gender =='F'])
    F_percent =  nbr_participants_F / (nbr_participants_M+nbr_participants_F)
    M_percent =  1 - F_percent

    avg_age = df.age.mean()
    avg_age_M = df[df.gender == 'M'].age.mean()
    avg_age_F = df[df.gender == 'F'].age.mean()

    # Data to plot
    labels = 'Male', 'Female'
    sizes = [M_percent, F_percent]
    # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    # explode = (0.1, 0, 0, 0)  # explode 1st slice
     
    # Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
     
    plt.axis('equal')
    plt.show()

    # print(nbr_participants_M)
    # print(nbr_participants_F)
    # print(M_to_F_ratio)
    # print(avg_age)
    # print(avg_age_M)
    # print(avg_age_F)

    # print(df.avgSpeed.describe())

