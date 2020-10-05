# -*- coding: utf-8 -*-
"""
Description:

At some point, the core data folks switched from negatives and positives to 
totals and positives. Theoretically, we can figure out what the totals were 
This is only for the states reporting test-race data: 
DE, IL, IN, KS, NV, RI, UT
"""

import pandas as pd
import numpy as np


df = pd.read_csv('/Users/mchappelka/Downloads/CTP/Race Data Entry - Tracker Commits.csv')



# subset to just the states we're interested in
states_list = ['DE', 'IL', 'IN', 'KS', 'NV', 'RI', 'UT']

# keep all rows with the states we're interested in, as well as with missing
# values or the word 'State"
states_df = df.loc[df['Unnamed: 1'].isin(states_list + ['State', np.nan], )]


# drop extraneous columns (notes, percentages, checks, etc): columns 23-37
states_df.drop(['Unnamed: 52',
                             'Unnamed: 53',
                             'Unnamed: 54',
                             'Unnamed: 55',
                             'Unnamed: 56',
                             'Unnamed: 57',
                             'Unnamed: 58',
                             'Unnamed: 59',
                             'Unnamed: 60',
                             'Unnamed: 61',
                             'Unnamed: 62',
                             'Unnamed: 63',
                             'Unnamed: 64',
                             'Unnamed: 65',
                             'Unnamed: 66',
                             'Unnamed: 67',
                             'Unnamed: 68',
                             'Unnamed: 69',
                             'Unnamed: 70']
               , axis=1, inplace=True)

# reformat the data so we have meaningful column names
columns = states_df.columns.tolist()
prefix = ''
midfix = ''

# iterate through each column name
for col_num in range(0, len(columns)):
    curr_col = columns[col_num]

    # if the current column name doesn't have 'Unnamed', that mean it's informative 
    # and we'll want to put it at the start of our new column name
    if 'Unnamed' not in curr_col:
        # create a prefix that is the 
        prefix = curr_col
        # the tests column is wordy, so let's just call it tests
        if 'Tests' in prefix:
            prefix = 'Tests'
        
    # The first row of the dataset is either missing or contains column info
    # if the first row for that column is not missing, it should be part of
    # the new column name
    if states_df.iloc[0][col_num] is not np.nan:
        midfix = states_df.iloc[0][col_num]
    
    # the main column name is in row 1 
    suffix = states_df.iloc[1][col_num]
        
    # create a new column name
    colname = prefix +  ' ' + midfix + ' ' + suffix
    
    # some column names have leading/trailing whitespace, let's remove it
    columns[col_num] = colname.strip()
    

# rename the column in the dataset to have the new column names
states_df.columns = columns
  
# drop any of the death data (since we're only interested in testing dating)      
cols = [c for c in states_df.columns if "Deaths" not in c and "%" not in c]
tests_df = states_df[cols]  


# now that we got all the information we need out of rows 0 and 1, drop them
clean_df = tests_df.iloc[2:]

#drop rows that are na for every column
clean_df = clean_df.dropna(how='all')

# create a dataset of just the negative tests
# need to convert date to integer in order to compare
clean_df.Date = clean_df["Date"].astype(int)
 
# 9/6 and earlier: Tests means negative tests
pre_df = clean_df.loc[clean_df["Date"] <= 20200906]

# change name of tests to negative
pre_df.columns = pre_df.columns.str.replace("Tests", "Negatives")

# create a totals column

# these are the variables we want totals for
test_vars = ['Race Known White', 
                'Race Known Black',
                'Race Known LatinX / Hispanic', 
                'Race Known Asian',
                'Race Known AIAN', 
                'Race Known NHPI',
                'Race Known Multiracial', 
                'Race Other',
                'Race Unknown', 
                'Ethnicity Known Hispanic',
                'Ethnicity Known Non-Hispanic',
                'Ethnicity Unknown Ethnicity']

# iterate through each variable and sum positive and negative to create total
for v in test_vars:
    print(v)
    # the ethnicity column names have slightly different names for positive
    # and negative tests
    if v == "Ethnicity Unknown Ethnicity":
        pre_df["Total " + v] =  pre_df["Positives " + v] + pre_df['Negatives Ethnicity Unknown'] 

    else:
        pre_df["Total " + v] =  pre_df["Positives " + v] + pre_df["Negatives " + v] 

# output
pre_df.to_csv("/Users/mchappelka/Downloads/CTP/tests_update.csv", index=False)

       
        
        
        
        
        
        
        
        
        