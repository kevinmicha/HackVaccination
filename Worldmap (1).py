#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install geopandas seaborn')
get_ipython().system('pip install plotly')


# In[4]:


import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px
import pandas as pd
convert_ISO_3166_2_to_1 = {

'Astralia':'AUS',
'Canada':'CAN',
'Germany':'DEU',
'China':'CHN',
'France':'FRA',
'India':'IND',
'Iran':'IRN',
'USA':'USA',
'UK':'GBR'
}

df2=pd.read_csv("df_simulated_tweets.csv")
df2["Location"] = df2["Location"].map(convert_ISO_3166_2_to_1)
df3=df2.groupby(["Location"]).sum()

df4=list(df2["Location"].unique());
df4 = sorted([x for x in df4 if pd.notna(x)])
data_geo = {
    'Country': df4,
    'Likes': df3['Likes']}

fig = px.choropleth(data_geo, locations='Country',
                    projection='natural earth',
                    color='Likes',
                    title='Negative vaccine posts per country')
fig.show()


# In[ ]:




