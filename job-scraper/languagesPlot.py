import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from collections import Counter

#read data
data = pd.read_csv('aswift_prog.csv', encoding = "ISO-8859-1")
data.head()
progData = data['Language'].values

#split all data so that each langauge is counted individually 
#e.g. c++ add 1 to c++ counter instead of having a separate data point like [c++ , scheme]
languagesArray = []
for languageItems in progData:
    languageItemArray = languageItems.split(",")
    for item in languageItemArray:
        item = item.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        languagesArray.append(item)

#plot piechart
labels = []
sizes = []

for x, y in Counter(languagesArray).items():
    labels.append(x)
    sizes.append(y)

#download piechart as progpie.png
plt.pie(sizes, labels=labels, radius=1)
plt.savefig("progpie.png")
plt.show()