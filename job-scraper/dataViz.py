#!/usr/bin/env python
# coding: utf-8

# In[2]:

import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from io import BytesIO
from matplotlib.figure import Figure

import aswiftScript


# In[3]:

def produce_pie():
    """Produce a pie chart from the data."""
    # Scrape the website and produce a new dataset
    aswiftScript.main()

    data = pd.read_csv(
            'ASWIFT-UK-industry=videogames-category=programming.csv',
            encoding = "ISO-8859-1"
            )
    data.head()
    data['Location'] = data['Location'].str.replace(', United Kingdom', '')
    locFreq = data['Location'].value_counts()
    locData = dict(locFreq)
    
    labels = []
    sizes = []
    
    
    for x, y in locData.items():
        labels.append(x)
        sizes.append(y)
        
    # PIE CHART 
    # With pyplot

    plt.pie(sizes, labels=labels)
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

    # breakpoint()
    # plt.show()

    # Without pyplot
    # pie = Figure()
    # breakpoint()
    # fig1, ax1 = pie.subplots()
    # ax1.pie(sizes, labels=labels)
    # ax1.axis("equal")

    # buf = BytesIO()
    # fig.savefig(buf, format="png")

    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return data

# In[4]:


# BAR CHART
# plt.figure(figsize=(12,6))
# plt.bar(labels, sizes)
# plt.xticks(rotation=90)
# plt.xlabel("Location")
# plt.ylabel("Frequency")
# plt.title("Frequency of jobs based on location")
# plt.show()


# In[ ]:




