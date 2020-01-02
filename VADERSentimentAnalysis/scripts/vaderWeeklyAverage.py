#NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# ### Include necessary packages for notebook 

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import csv
import json
import calendar
import time
from datetime import date, timedelta
import re
import string
import glob
import zipfile
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib


# Variables

source = "*"
vaderScores = []
allVaderScores = []
weeklyDates = []
vaderSum = 0
weekNum = 0
stopDate = date(1111,1,11)
currentDate = date(1111, 1, 1)


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath,'Text-Analysis-master','data','twitter')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')


# Shorten SentimentIntensityAnalyzer Function

vader = SentimentIntensityAnalyzer()


# Functions

def getMonthNumber(month):
    if month == "Jan":
        return 1
    elif month == "Feb":
        return 2
    elif month == "Mar":
        return 3
    elif month == "Apr":
        return 4
    elif month == "May":
        return 5
    elif month == "Jun":
        return 6
    elif month == "Jul":
        return 7
    elif month == "Aug":
        return 8
    elif month == "Sep":
        return 9
    elif month == "Oct":
        return 10
    elif month == "Nov":
        return 11
    else:
        return 12

def nextWeekString(year, month, day):
    nextDate = date(year, month, day) + timedelta(1)
    return nextDate
    
def getMonthFromFile(created_at):
    return getMonthNumber(created_at[4:7])

def getDayFromFile(created_at):
    return int(created_at[8:10])

def getYearFromFile(created_at):
    return int(created_at[26:])

#scores tweet using vader and returns the compound
def scoreVader(text):
    vs = vader.polarity_scores(text)
    return vs['compound']



def lines2list(filepath, encoding = 'utf-8', commentChar = None):
    
    with open(filepath, 'r', encoding = encoding) as f:
        lines = f.readlines()
        
        if commentChar is not None:
            lines = [x for x in lines if not x.startswith(commentChar)]
        
        # strip each line
        lines = [x.strip() for x in lines]
        
        # eliminate empty lines  
        lines = [x for x in lines if x]  
        
    return lines

def isAscii(s):
    return all(ord(c) < 128 for c in s)



# nzip files

direct = os.path.join(dataHome, "JSON")
allZipFiles = glob.glob(os.path.join(dataHome, "JSON","*.zip"))
for item in allZipFiles:
    fileName = os.path.splitext(direct)[0]
    zipRef = zipfile.ZipFile(item, "r")
    zipRef.extractall(fileName)
    zipRef.close()
    os.remove(item)


#  Read the 'text' and 'created_at' key in the JSON file

for file in glob.glob(os.path.join(dataHome, "JSON", source+".json")):
    with open(file, mode = 'r', encoding = "utf8") as read:
        #if a file starts a new week, currentDate and stopDate must be initialized
        if weekNum == 0:
            first = json.loads(next(read))
            created_at = first['created_at']
            month = getMonthFromFile(created_at)
            day = getDayFromFile(created_at)
            year = getYearFromFile(created_at)
            currentDate = date(year, month, day)
            stopDate = nextWeekString(year, month, day)
               
        for line in read:
            data = json.loads(line)
            created_at = data['created_at']
            currentMonth = getMonthFromFile(created_at)
            currentDay = getDayFromFile(created_at)
            currentYear = getYearFromFile(created_at)
            currentDate = date(currentYear, currentMonth, currentDay)
            if currentDate >= stopDate:
                vaderMean = vaderSum / weekNum
                vaderScores.append(vaderMean)
                weeklyDates.append(currentDate)
                vaderSum = 0
                weekNum = 0
                month = stopDate.month
                day = stopDate.day
                year = stopDate.year
                currentDate = date(year, month, day)
                stopDate = nextWeekString(year, month, day)
            vaderScore = scoreVader(data['text'])
            vaderSum += vaderScore
            
            allVaderScores.append(vaderScore)
            weekNum += 1
                
        
        print("Finished reading " + str(file))
        
#if there is unsaved data
if(weekNum != 0): 
    vaderMean = vaderSum / weekNum
    vaderScores.append(vaderMean)
    weeklyDates.append(currentDate)


# Save results as .csv file

with open(os.path.join(dataResults, 'vaderWeeklyScores.csv'), "w") as write:
    writer = csv.writer(write)
    writer.writerows([vaderScores])
    writer.writerows([weeklyDates])


# Plot the graph

# Variables
vaderGraphOutput = 'vaderSentimentAvgOverTime.png'
fmt = 'png'
dpi = 300
figSz = (30,10)
dateFormat = '%m/%d/%Y'
interval = 1
labelX = 'Time'
labelY = 'Score'
labelTitle = 'Sentiment Shift About Government Shutdown Over Time\nDecember 22, 2018 - January 23, 2019'
labelFont = 30
tickFont = 20
rotate = 45
beginDate = date(2018, 12,22)
endDate = date(2019, 1, 23)


#Plot graph
fig = plt.figure(figsize=figSz)
ax = plt.subplot()
ax.plot(weeklyDates, vaderScores, label = 'Avg. VADER Score', linewidth = 4)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
ax.xaxis.set_major_locator(mdates.DayLocator(interval = interval))
ax.grid()
ax.axhline(color = 'black')
ax.legend(loc = 4, prop = {'size':labelFont})

plt.xlabel(labelX, fontsize = labelFont)
plt.ylabel(labelY, fontsize = labelFont)
plt.title(labelTitle, fontsize = labelFont)
plt.xticks(size = tickFont, rotation = rotate)
plt.yticks(size = tickFont)
plt.xlim((beginDate, endDate))

plt.show()
fig.savefig(os.path.join(dataResults, vaderGraphOutput), format=fmt, dpi=dpi, bbox_inches='tight')

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
