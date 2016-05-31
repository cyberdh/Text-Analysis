#Top Ten Words in Hamlet, Curated Stopwords Removed

#Set the working directory
setwd("~/Desktop/R/Text_Analysis/data/shakespeareFolger/")


#Call libraries used in the script
#library(wordcloud)
#library(tm)
#library(Rcolorbrewer)

#Read in the text 
text_raw<-scan("Hamlet.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeWords, stopwords("SMART"))
corpus <- tm_map(corpus, removePunctuation)

