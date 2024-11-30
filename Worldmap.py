#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install geopandas seaborn')
get_ipython().system('pip install plotly')


# In[2]:


import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px
import pandas as pd
data_geo = {
    'Country': ['GBR', 'CHN', 'USA', 'IR', 'DEU', 'AUS', 'CAN', 'RUS', 'CN'],
    'NegativePostCount': [4, 2, 2, 1, 2, 1, 7, 3, 9]}

fig = px.choropleth(data_geo, locations='Country',
                    projection='natural earth',
                    color='NegativePostCount',
                    title='Negative vaccine posts per country')
fig.show()


# In[ ]:




