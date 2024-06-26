import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = np.where(df["weight"]*10000/(np.square(df['height'])) > 25 ,1,0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["gluc"] = np.where(df['gluc']>1,1,0)
df["cholesterol"] = np.where(df['cholesterol']>1,1,0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt( id_vars='cardio',value_vars=['cholesterol','gluc','smoke','alco','active','overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(df_cat['cardio']).value_counts().to_frame()

    # Draw the catplot with 'sns.catplot()'

    # Get the figure for the output
    fig = sns.catplot(data=df_cat, kind = 'bar', x= "variable", hue = 'value',y='count', col ='cardio')


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[np.where((df['ap_lo'] <= df['ap_hi'])&
                       (df['height'] >= df['height'].quantile(0.025))&
                       (df['height'] <= df['height'].quantile(0.975))&
                       (df['weight'] >= df['weight'].quantile(0.025))&
                       (df['weight'] <= df['weight'].quantile(0.975)))]
    # Calculate the correlation matrix
    corr = df_heat.corr(method = "spearman").round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))


    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr , annot = True, mask=mask)
    

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
draw_heat_map()