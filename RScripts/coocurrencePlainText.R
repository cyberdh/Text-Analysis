#Top Ten Words in Hamlet, Curated Stopwords Removed

library(tm)
library(RWeka)

#Set the working directory
setwd("~/Documents/IU/CyberDH/Text_Analysis/data/")

#Read in the text 
#text_raw<-scan("Hamlet.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(DirSource("shakespeareFolger"))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeWords, stopwords("SMART"))
corpus <- tm_map(corpus, removeWords, c("tis", "hath"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
#corpus <- tm_map(corpus, PlainTextDocument)

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)
findAssocs(dtm, "love", .6)

