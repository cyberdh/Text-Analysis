#Top Ten Words in Hamlet, Curated Stopwords Removed

library(tm)
library(igraph)

#Set the working directory
setwd("~/Desktop/R/Text_Analysis/data/")

#Read in the text 
#text_raw<-scan("Hamlet.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(DirSource("shakespeareFolger"))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords" to line 19
myStopWords <- scan("~/Desktop/R/Text_Analysis/data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
#corpus <- tm_map(corpus, PlainTextDocument)
#￼# keep a copy of corpus to use later as a dictionary for stem
# completion
#corpusCopy <- corpus
# stem words
#myCorpus <- tm_map(corpus, stemDocument)
# stem completion
#myCorpus <- tm_map(corpus, content_transformer(stemCompletion), dictionary = corpusCopy, lazy=TRUE)
termDocMatrix <- TermDocumentMatrix(corpus, control = list(wordLengths = c(1, Inf)))
termDocMatrix <- as.matrix(termDocMatrix)
# change it to a Boolean matrix
termDocMatrix[termDocMatrix>=1] <- 1
# transform into a term-term adjacency matrix
termMatrix <- termDocMatrix %*% t(termDocMatrix)
# build a graph from the above matrix
g <- graph.adjacency(termMatrix, weighted=T, mode = "undirected")
# remove loops
g <- simplify(g)
# set labels and degrees of vertices
V(g)$label <- V(g)$name
V(g)$degree <- degree(g)
# set seed to make the layout reproducible
set.seed(3952)
layout1 <- layout.fruchterman.reingold(g)
plot(g, layout=layout1)