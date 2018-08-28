#Top Ten Words #NeverAgain, Curated Stopwords Removed
#Call libraries used in the script
#Set the working directory
setwd("~/Text-Analysis/")

#Call libraries used in the script
library(NLP)
library(tm)
library(dplyr)
library(tidytext)

#unzip file
zipF<- "data/twitter/neverAgain.csv.zip"
outDir<-"data/twitter"
unzip(zipF,exdir=outDir)

#Read in the text 
tweets <- read.csv("data/twitter/neverAgain.csv")

#Create a corpus 
corpus <- iconv(tweets$text, to = "utf-8")
corpus <- VCorpus(VectorSource(corpus))

corpus <- tm_map(corpus, function(x) iconv(x, "ASCII", "UTF-8", sub=""))

#Clean the corpus
corpus <- tolower(corpus)
corpus <- removePunctuation(corpus)
corpus <- removeNumbers(corpus)
corpus <- stripWhitespace(corpus)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
corpus <- removeURL(corpus)
corpus <- removeWords(corpus, c(stopwords("english"), 'na','amp','rt', 'neveragain', 'dont', 'will', 'see','just', 'emmachange', 'xokarminox'))

myCorpus <- as.character(corpus)

#Convert to data frame (helps make plot labeling easier)
freqDF <- data_frame(myCorpus) %>%
  unnest_tokens(word, myCorpus) %>%
  count(word, sort = TRUE)

head(freqDF)

#freqDF <- freqDF[-1,]

#head(freqDF)

labNames <- head(freqDF$word, 10)

write.csv(head(freqDF, 100), "~/freqWordsNeverAgain.csv")

#Remix ideas: 1) Play around with the number of word on the chart by changing it from "10"
# 2) Don't forget to adjust your plot's title if you have changed the input text
# 3) Look up the frequency of all the words in the corpus by typing "freq" into the console

par(mar=c(8,5,3,1))
x <- barplot(head(freqDF$n,10), ylim=c(0,8000), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen"),col.main="gold", col.lab="red",
             main="Tweet Word Frequency", xlab="", ylab="Number of Occurences", xaxt="n")
axis(2, at=x, labels=TRUE)
axis(2, col="gray27", col.axis="gray27", col.ticks="gray27",labels=TRUE)
text(x, par("usr")[3], srt=45, adj=c(1.1,1.5), xpd = TRUE, labels = labNames, cex=.9, col="gray27")
title(xlab='Top Ten Words', line=5, col.lab="red")
print(x)



