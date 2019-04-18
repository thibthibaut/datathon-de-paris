#!/usr/bin/env python

import json
import numpy as np
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"



def plotMeanSpeedPerAge(df):
    # MEAN SPEED PER AGE
    mspac = [0]*150
    mspas = [0.0]*150
    mspa_20pc = [ [] for x in range(150) ]
    mspa_20pc_mean = [0.0]*150
    for c in df.values:
        mspac[c[4]]+=1
        mspas[c[4]]+=c[6]
        mspa_20pc[c[4]].append(c[6])
    
    for i in range(150):
        if (mspac[i] != 0):
            mspas[i] /= float(mspac[i])
            mspa_20pc[i] = mspa_20pc[i][:int(0.20*len(mspa_20pc[i]))]
            mspa_20pc_mean[i] = np.mean(mspa_20pc[i])
            # print(mspa_20pc[i][0])

    # print(mspas[22])
    # print(mspa_20pc_mean[22])

    mspa = pd.DataFrame(columns=['age', 'mean_speed'])
    mspa_20pc_df = pd.DataFrame(columns=['age', 'mean_speed_top_20pc'])
    for i in range(18, 91):
        if mspac[i] != 0:
            mspa = mspa.append({'age': i, 'mean_speed': mspas[i]}, ignore_index=True)
            mspa_20pc_df = mspa_20pc_df.append({'age': i, 'mean_speed_top_20pc': mspa_20pc_mean[i]}, ignore_index=True)

    fig, ax = plt.subplots()
    sns.scatterplot(x=mspa.age, y=mspa.mean_speed, ax=ax)
    sns.scatterplot(x=mspa_20pc_df.age, y=mspa_20pc_df.mean_speed_top_20pc, ax=ax)

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
    sns.set(style="darkgrid")

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
    # labels = 'Male', 'Female'
    # sizes = [M_percent, F_percent]
    # Plot
    # plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    # plt.axis('equal')


    # print(df.finishTime.values.dtype)
    
    bins = np.linspace(2*60*60, 7*60*60, num=200, dtype=int )
    ages = pd.to_numeric(df.age)
    ages_F = pd.to_numeric(df[df.gender == 'F'].age)
    ages_M = pd.to_numeric(df[df.gender == 'M'].age)

    arrival_times = pd.to_numeric(df.finishTime)

    # sns.distplot(arrival_times, bins=bins, hist=True, kde=False, axlabel='Finish time in seconds, slices of 90 seconds', color='r').set_title('Distribution of arrival time')

    # sns.jointplot(x=ages, y=arrival_times, xlim=(15, 90), kind='scatter')

    # AGE HISTO
    # bins = np.linspace(17, 90, num=90-17+2, dtype=int )
    # fig, ax = plt.subplots()
    # sns.distplot(ages_F, bins=bins, norm_hist=False, kde=False, color='g',  ax=ax)
    # sns.distplot(ages_M, bins=bins, norm_hist=False, kde=False, ax=ax)


    plotMeanSpeedPerAge(df)
    # print(nbr_participants_M)
    # print(nbr_participants_F)
    # print(M_to_F_ratio)
    # print(avg_age)
    # print(avg_age_M)
    # print(avg_age_F)
    # plt.hist(df.finishTime)

    # print(df.avgSpeed.describe())
    plt.show()
