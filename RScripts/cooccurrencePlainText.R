#Top Ten Word Co-occurrence, Curated Stopwords Removed

library(knitr)
library(markdown)
library(rmarkdown)
library(NLP)
library(tm)


#Set the working directory
setwd("~/Desktop/Text-Analysis/data/")


#Create a corpus 
corpus <- Corpus(DirSource("~/Desktop/Text-Analysis/data/shakespeareFolger/"))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords
myStopWords <- scan("~/Desktop/Text-Analysis/data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)

#Create matrix using DocumentTermMatrix function and saving it as "dtm"
dtm <- DocumentTermMatrix(corpus)

#Find overall frequency 
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)

#Find results: NOTE: for this to work, you must first click the "Source" button in the source box and then run the findAssocs script in the Console on the bottom left in RStudio. It must be done in that order.
findAssocs(dtm, "father", .6)
#findAssocs(dtm, "love", .6)
