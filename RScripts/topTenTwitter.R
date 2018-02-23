#Top Ten Words #NeverAgain, Curated Stopwords Removed
#Call libraries used in the script
#Set the working directory
setwd("~/Text-Analysis/")

#Call libraries used in the script
library(tm)
library(twitteR)

#unzip file
zipF<- "data/twitter/neverAgain.csv.zip"
outDir<-"data/twitter"
unzip(zipF,exdir=outDir)

#Read in the text 
tweets <- read.csv("data/twitter/neverAgainSnippet.csv")

#Create a corpus 
corpus <- iconv(tweets$text, to = "utf-8")
corpus <- Corpus(VectorSource(corpus))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(function(x) iconv(x, "ASCII", "UTF-8", sub="")))
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords
myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
corpus <- tm_map(corpus, content_transformer(removeURL))
corpus <- tm_map(corpus, removeWords, c(stopwords("english"), myStopWords, 'amp','rt','neveragain','dont'))

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)

#Convert to data frame (helps make plot labeling easier)
freqDF <- as.data.frame.character(freq)
freqDF$words <- rownames(freqDF)

labNames <- head(freqDF$words, 10)

#Remix ideas: 1) Play around with the number of word on the chart by changing it from "10"
# 2) Don't forget the adjust your plot's title if you have changed the input text
# 3) Look the frequency of all the words in the corpus by typing "freq" into the console

par(mar=c(8,5,3,1))
x <- barplot(head(freq,10), ylim=c(0,8000), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen"), col.lab="black",
     main="Tweet Word Frequency", xlab="", ylab="Number of Occurences", xaxt="n")
axis(2, at=x, labels=TRUE)
text(x, par("usr")[3], srt=45, adj=c(1.1,1.5), xpd = TRUE, labels = labNames, cex=.9)
title(xlab='Top Ten Words', line=5)
print(x)



