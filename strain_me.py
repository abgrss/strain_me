### STRAIN_ME.PY
### SUGGESTS THREE CANNABIS STRAINS FOR USER-ENDERED FLAVOUR, EFFECT, AND MEDICAL USE

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored, cprint
pd.set_option('display.max_columns', None)

# IMPORT CSVs
# Assumes "data" folder in same directory as program
df_strain_me = pd.read_csv('df_strain_me.csv', encoding = "ISO-8859-1")

# FLAVOURS, EFFECTS, MEDICALS
flavours = ['sweet', 'strawberry', 'earthy', 'blue cheese', 'sage', 'honey', 'rose', 'tree fruit', 'violet', 'coffee', 'pear', 'spicy/herbal', 'tropical','pungent', 'tea', 'apricot', 'mint', 'pepper', 'flowery', 'ammonia', 'blueberry', 'berry', 'chemical', 'pine', 'woody', 'lime', 'plum', 'nutty', 'citrus', 'orange', 'mango', 'diesel', 'lemon', 'pineapple', 'apple', 'grape', 'menthol', 'chestnut', 'skunk', 'grapefruit', 'peach', 'butter', 'lavender', 'tar', 'tobacco', 'vanilla']
effects = ['focused', 'dizzy', 'energetic', 'happy', 'happy', 'creative', 'sleepy', 'tingly', 'aroused', 'anxious', 'uplifted', 'headache', 'talkative', 'paranoid', 'hungry', 'giggly', 'relaxed', 'euphoric']
medicals = ['inflammation', 'lack of appetite', 'stress', 'fatigue', 'cramps', 'nausea', 'muscle spasms', 'depression', 'pain', 'eye pressure', 'headaches', 'insomnia']

# CREATE DF TO QUERY: df_rec
df_rec = df_strain_me.copy()

# CREATE "MORE" FUNCTIONALITY
morelist_effects = []
morelist_flavours = []
morelist_medicals = []

for i in df_rec.columns: # Populate morelist_effects
    if i in effects:
        morelist_effects.append(i)

for i in df_rec.columns: # Populate morelist_flavours
    if i in flavours:
        morelist_flavours.append(i)

for i in df_rec.columns: # Populate morelist_medicals
    if i in medicals:
        morelist_medicals.append(i)

# SAME FUNCTION AS IN strain_minfo.py
def plot_effmed(strain):
    """
    Plots bar charts for effects and medical uses for a given strain
    Sample input: "strain_series = df.iloc[strain_index]"
    """

    strain = strain.dropna()

    strain_num = strain.drop(['strain', 'strain_type'])
    # print(strain_num)
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
    plt.title(f'Effects - {strain.strain}', fontsize=16)
    
    plt.subplot(1,2,2)
    sns.barplot(y=ym, x=xm)
    plt.xlabel('Frequency (% of reviews)', fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(f'Medical uses - {strain.strain}', fontsize=16)

    plt.tight_layout()
    plt.show();
    return None

def strain_me():
    """
    Prompts user for an effect, medical symptom, and flavour
    Recommends three strains.
    Identifies their clusters (with cluster name).
    )
    """

    bad_entries = 0 # a counter for silently keeping track of incorrect entries
    cutoff = 0.9 # Initial cutoff for effects. Default is 90% 
    thecolor = 'cyan' # custom highlight colour for cmd line output

    os.system('clear') # clears the screen

    effect = input(f"\nHi! I'm Strain{colored('_', 'green')}me! I can help recommend cannabis strains for you!\n\nPlease enter an {colored('EFFECT', thecolor)} you\'re looking to experience.\nMost popular effects: relaxed, happy, euphoric, uplifted, sleepy, creative, energetic\n>>> ")

    if effect == "more": # USER INPUTS "MORE"
        print(morelist_effects)
        effect = input(">>> ")

    if effect not in effects: # If entered EFFECT is unknown
    	effect = "relaxed" # Most common effect
    	bad_entries = bad_entries + 1

    flavour = input(f"\nGreat! Please enter a {colored('FLAVOUR', thecolor)} you'd like your cannabis to have.\nMost popular flavours: earthy, sweet, citrus, pungent, berry\n>>> ")

    if flavour == "more": # USER INPUTS "MORE"
        print(morelist_flavours)
        flavour = input(">>> ")

    if flavour not in flavours: # If entered FLAVOUR is unknown
    	flavour = "earthy" # Most common effect
    	bad_entries = bad_entries + 1

    medical = input(f"\nExcellent! Please enter a {colored('MEDICAL SYMPTOM', thecolor)} you're looking to alleviate.\nMost (un)popular symptoms: stress, depression, pain, insomnia, fatigue\n>>> ")

    if medical == "more": # USER INPUTS "MORE"
        print(morelist_medicals)
        medical = input(">>> ")
    
    if medical not in medicals: # If entered MEDICAL is unknown
    	medical = "stress" # Most common effect
    	bad_entries = bad_entries + 1    	


    # Generate df_temp from user-entered EFFECT, MEDICAL, FLAVOUR
    no_flavours = False # Set to true if no exact match found for effect/medical/flavour
    no_medicals = False # Set to true if no exact match found for effect/medical

    done = False
    while(done == False):
        # Generate df_temp
        df_temp = df_rec.copy()
        df_temp = df_temp[df_temp[flavour] == 1.0] # FLAVOUR
        # print(flavour, len(df_temp.index)) # NUMBER OF STRAINS AFTER FLAVOUR SELECTION
        df_temp = df_temp[df_temp[effect] > cutoff] # EFFECT
        # print(effect, len(df_temp.index)) # NUMBER OF STRAINS AFTER EFFECT SELECTION     
        df_temp = df_temp[df_temp[medical] > cutoff] # MEDICAL
        # print(medical, len(df_temp.index)) # NUMBER OF STRAINS AFTER MEDICAL SELECTION

        # CHECK IF THERE IS AT LEAST 3 ITEMS THAT MATCH THE CONDITIONS
        # IF NOT, REDUCE THE CUTOFF AND CREATE A NEW df_temp
        if len(df_temp.index) > 2: # If 3 items or more
            done = True
            print(f'{len(df_temp.index)} exact matches found.')
        else:
            if cutoff < 0.01: # If cutoff reduced all the way to 0
                done = True
                no_flavours = True # Try again, but without the specified flavour
                print(f'{len(df_temp.index)} exact matches found. Dropping flavour.')
            else:
                cutoff = cutoff - 0.1 # reduce the cutoff by 10%

    if no_flavours == True: # If no matches, generate a df_temp just for EFFECT, MEDICAL
	    done = False
	    while(done == False):
	        # Generate a df_temp
	        df_temp = df_rec.copy()
	        df_temp = df_temp[df_temp[effect] > cutoff] # EFFECT
	        df_temp = df_temp[df_temp[medical] > cutoff] # MEDICAL
	 
	        if len(df_temp.index) > 2: # If 3 items or more
	            done = True
	            print(f'{len(df_temp.index)} exact matches found.')
	        else:
	            if cutoff < 0.01: # If cutoff reduced all the way to 0
	                done = True
	                no_medicals = True
	                print(f'{len(df_temp.index)} exact matches found. Dropping medical use.')
	            else:
	                cutoff = cutoff - 0.1 # reduce the cutoff by 10%

    if no_medicals == True: # If no matches, generate a df_temp just for EFFECT,
	    done = False
	    while(done == False):
	        # Generate a df_temp
	        df_temp = df_rec.copy()
	        df_temp = df_temp[df_temp[effect] > cutoff] # EFFECT
	 
	        if len(df_temp.index) > 2: # If 3 items or more
	            done = True
	            print(f'{len(df_temp.index)} exact matches found.')
	        else:
	            if cutoff < 0.01: # If cutoff reduced all the way to 0
	                done = True
	                print(f'{len(df_temp.index)} exact matches found.')
	            else:
	                cutoff = cutoff - 0.1 # reduce the cutoff by 10%

    # Select 3 strains
    try:
        df_sample = df_temp.sample(3)
    except: # WORST CASE SCENARIO - NOT EVEN 3 MATCHING SAMPLES FOR EFFECTS IN df_temp
    	df_sample = df_rec.sample(3)

    strain_1 = df_sample.iloc[0]
    strain_2 = df_sample.iloc[1]
    strain_3 = df_sample.iloc[2]

    # Get the strain clusters
    clusters = {0:'Lemon Leaves', 1:'Lights Out', 2:'Berry Relaxed', 3:'Rise and Shine'}
    
    cluster_1 = df_strain_me[df_strain_me.strain == strain_1['strain']].cluster.values[0]
    cluster_2 = df_strain_me[df_strain_me.strain == strain_2['strain']].cluster.values[0]
    cluster_3 = df_strain_me[df_strain_me.strain == strain_3['strain']].cluster.values[0]

    # Set cluster output color
    colordict = {0:'yellow', 1:'magenta', 2:'cyan', 3:'green'}
    colred = 'red'

    color_1 = colordict[cluster_1]
    color_2 = colordict[cluster_2]
    color_3 = colordict[cluster_3]

    num_flav = strain_1[flavours].dropna().index

    z = " "

    print(f"{z*bad_entries}---------------------")

    print(f"\n\nMay I suggest {colored(strain_1.strain.upper(), color_1)}, {colored(strain_2.strain.upper(), color_2)}, or {colored(strain_3.strain.upper(), color_3)}?")
    
    # PRINT STRAIN CLUSTER
    # FOR MORE INFORMATION ON STRAIN CLUSTERS, SEE CLUSTERING REPOSITORY
    # print(f'\n{colored(strain_1.strain.upper(), color_1)} is a member of the {colored(clusters[cluster_1].upper(), color_1)} group.')

    if len(num_flav) == 3:
        print(f'\nReviewers describe {colored(strain_1.strain.upper(), color_1)}\'s flavour as {colored(num_flav[0], colred)}, {colored(num_flav[1], colred)}, and {colored(num_flav[2], colred)}.')
    elif len(num_flav) == 2:
        print(f'\nReviewers describe {colored(strain_1.strain.upper(), color_1)}\'s taste as {colored(num_flav[0], colred)} and {colored(num_flav[1], colred)}.')
    elif len(num_flav) == 1:
        print(f'\nReviewers describe {colored(strain_1.strain.upper(), color_1)}\'s taste as {colored(num_flav[0], colred)}.')
    else:
        print(f'\nAlas! There are no flavours for this strain.')
    
    print(f"\nPress Enter to see effects/medical usage data for {colored(strain_1.strain.upper(), color_1)}.")

    input() # wait until any key is pressed

    # For strain 1 just keep numerical data, no dry_mouth or dry_eyes (removed from df)
    plot_effmed(strain_1)
    
    return None

#### THE ACTUAL PROGRAM ####
while 1==1:
    strain_me()

