
# coding: utf-8

# Document Similarity Heatmap

# Run CyberDH environment

# NOTE: This chunk of code is only for use with Research Desktop.
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Getting your data
# File paths
homePath = os.environ["HOME"]
cleanedData = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "LSA", "cleanedData")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
cleanedCSV = os.path.join(cleanedData, "docSimilarityMatrix.csv")


# Read in .csv file
csvDF = pd.read_csv(cleanedCSV)
df = pd.DataFrame(csvDF)
sdf = df.set_index(df["Unnamed: 0"])
del sdf.index.name
del sdf["Unnamed: 0"]
sdf


# Plot Heatmap
#Variables
heatmapFileName = 'DocSimHeatmap.svg'
dpi = 300
colorScheme = 'RdYlGn'
fontScale = 1

# Plot
figureSize = len(sdf)
sns.set(rc={'figure.figsize':(figureSize + 10, figureSize)}, font_scale = fontScale)
ax = sns.heatmap(sdf, cmap = colorScheme)
ax.figure.savefig(os.path.join(dataResults, heatmapFileName), dpi = dpi, bbox_inches='tight')
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()