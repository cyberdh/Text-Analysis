#Word Correlation, Curated Stopwords Removed
#Set the working directory
setwd("~/Text-Analysis/")

#load necessary packages
library(NLP)
library(tm)

options(mc.cores=1)

#Create a corpus
text_raw <- scan("data/shakespeareFolger/Hamlet.txt", what="character", sep="\n")
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords
myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("english"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)

chunk.size <- 500
x <- seq_along(corpus)
text.chunks <- split(corpus, ceiling(x/chunk.size))

corpus.chunk <- Corpus(VectorSource(text.chunks))
#Create matrix using DocumentTermMatrix function and saving it as "dtm"
dtm <- DocumentTermMatrix(corpus.chunk)
#remove sparse terms. If a word is absent from 40% of the chunks, it will be removed. 
dtms <- removeSparseTerms(dtm, 0.4)

#Find overall frequency 
freq <- sort(colSums(as.matrix(dtms)), decreasing = TRUE)

#Find results: NOTE: for this to work, you must first click the "Source" button in the source box and then run the findAssocs script in the Console on the bottom left in RStudio. It must be done in that order.
findAssocs(dtms, "father", .6)
#findAssocs(dtms, "love", .6)
