### STRAIN_INFO.PY
### PROVIDES FLAVOUR, EFFECT, AND MEDICAL USE INFO FOR USER-ENTERED CANNABIS STRAIN NAME

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sys
from termcolor import colored, cprint
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# SAME FUNCTION AS IN strain_me.py
def plot_effmed(strain_series):
    """
    Plots bar charts for effects and medical uses for a given strain
    Sample input: "strain_series = df.iloc[strain_index]"
    """
    strain_series = strain_series.dropna()
    strain_name = strain_series.strain

    strain_num = strain_series.drop(['strain', 'strain_type'])
    strain_num = strain_num.sort_values(ascending=False)

    xe = strain_num[strain_num.index.isin(effects)].values
    ye = strain_num[strain_num.index.isin(effects)].index

    xm = strain_num[strain_num.index.isin(medicals)].values
    ym = strain_num[strain_num.index.isin(medicals)].index

    plt.figure(figsize=(14,8))
    
    plt.subplot(1,2,1)
    sns.barplot(y=ye, x=xe)
    plt.xlabel('Frequency (% of reviews)', fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(f'Effects - {strain_name}', fontsize=16)
    
    plt.subplot(1,2,2)
    sns.barplot(y=ym, x=xm)
    plt.xlabel('Frequency (% of reviews)', fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(f'Medical uses - {strain_name}', fontsize=16)

    plt.tight_layout()
    plt.show();
    return None


os.system('clear') # clears the screen)

df = pd.read_csv('df_strain_me.csv')

effects = ['focused', 'dizzy', 'energetic', 'happy',\
           'creative', 'sleepy', 'tingly', 'aroused', 'anxious',\
           'uplifted', 'headache', 'talkative', 'paranoid', 'hungry',\
           'giggly', 'relaxed',  'euphoric']

medicals = ['inflammation', 'lack of appetite', 'stress', 'muscle spasms',\
            'nausea', 'fatigue', 'cramps', 'depression', 'pain', 'seizures',\
            'spasticity', 'eye pressure', 'headaches', 'insomnia']

flavours = ['sweet', 'strawberry', 'earthy', 'blue cheese', 'sage', 'honey', 'rose',\
			'tree fruit', 'violet', 'coffee', 'pear', 'spicy/herbal', 'tropical',\
			'pungent', 'tea', 'apricot', 'mint', 'pepper', 'flowery', 'ammonia', \
			'blueberry', 'berry', 'chemical', 'pine', 'woody', 'lime', 'plum' 'nutty', \
			'fruit', 'citrus', 'orange', 'mango', 'diesel', 'lemon', 'pineapple',\
			'apple', 'grape', 'menthol', 'chestnut', 'skunk', 'grapefruit',\
			'peach', 'butter', 'lavender', 'tar', 'tobacco', 'vanilla']

strain_series = df.strain.str.lower() # Gets a series of all strain names (lowercase names)

known_strain = False

strain = input("\nPlease enter a strain (don't worry about capitalization)\n>>> ")

while known_strain == False: # while the strain name is not in the dataframe...
    strain = strain.lower()
    if strain in list(strain_series): # if the strain name is in the list of strain names (lowercase)
        known_strain = True
    else:
        strain = input("\nStrain not known. Please try again\n>>> ")

strain_index = strain_series[strain_series == strain].index[0] # gets the df index for the strain

strain_series = df.iloc[strain_index] # selects only the relevant strain_series

f = strain_series[flavours].dropna().index

print(f"\nFlavours for {strain.upper()}:")
for flavour in f:
    print(f"- {flavour}")

print(f'\nPress Enter to see effects/medical usage data for {strain.upper()}.')

input() # wait until any key is pressed

plot_effmed(strain_series)