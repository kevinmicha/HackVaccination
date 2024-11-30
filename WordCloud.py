#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install wordcloud')


# In[2]:


import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[4]:


# Start with one review:
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("df_simulated_tweets.csv")
text = df.Keywords.str.cat(sep=' ')


# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:




