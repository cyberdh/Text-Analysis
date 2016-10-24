#Top Ten Words in Hamlet, Curated Stopwords Removed
#Call libraries used in the script
library(tm)

#Set the working directory
setwd("~/Desktop/R/Text_Analysis/data/shakespeareFolger/")

#Read in the text 
text_raw<-scan("Hamlet.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords" to line 19
myStopWords <- scan("~/Desktop/R/Text_Analysis/data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, stemDocument) # reduce word forms to stems


tdm <- TermDocumentMatrix(corpus)
p <- tmIndex(corpus, FUN = searchFullText,
             "love", doclevel = TRUE)
sum(p)

