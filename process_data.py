#!/usr/bin/env python

import json
import numpy as np
import pandas as pd

# Create a structured array to hold the data


dataframe = pd.DataFrame(columns=['firstName', 'lastName'])
# data = np.recarray(2 ,
#     dtype=[ ('firstName', 'U100'), ('lastName', 'U100') ] )


with open('./marathon_data_sanitized.json') as raw_file:
    json_data = json.load(raw_file)
    for chunk in json_data['data']:
        for competitor in chunk['items']:
            person = competitor['person']
            dataframe.append({'firstName': person['firstName'],
                              'lastName': person['lastName']}, ignore_index=True)
            
print(dataframe)


