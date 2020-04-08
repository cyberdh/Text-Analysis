
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
import plotly.graph_objs as go
import plotly as py


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
heatmapFileName = 'DocSimHeatmap.html'
colorScheme = 'RdYlGn'
wide = 1000
tall = 1000
tickFntSz = 10
titleFntSz = 20
mainTitle = "Document Similarity of Shakespeare's Plays"

# Plot
fig = go.Figure(data = go.Heatmap(z=sdf, x = sdf.index, y = sdf.columns, type = 'heatmap', colorscale = colorScheme,
                                  hovertemplate = "<b>Document Left</b>: %{y}<br>" + "<b>Document Bottom</b>: %{x}<br>" + "<b>Similarity Score</b>: %{z}",
                                  name = "Document Similarity"))

fig.update_layout(title={"text": mainTitle, 'y':0.95, 'x':0.55, 'xanchor': 'center', 'yanchor':'top'},titlefont = {"size":titleFntSz},
                  autosize = False, width = wide, height = tall, xaxis = dict(tickfont = dict(size = tickFntSz)), yaxis = dict(tickfont=dict(size=tickFntSz)))
py.offline.plot(fig, filename=os.path.join(dataResults, heatmapFileName))
fig.show()