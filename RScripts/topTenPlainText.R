#Top Ten Words in Hamlet, Curated Stopwords Removed

#Set the working directory
setwd("~/Desktop/R/Text_Analysis/data/shakespeareFolger/")


#Call libraries used in the script
library(tm)


#Read in the text 
text_raw<-scan("MidsummerNightsDream.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeWords, stopwords("SMART"))
corpus <- tm_map(corpus, removeWords, c("tis", "hath"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, PlainTextDocument)

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)


plot(head(freq, 100), type="b", lwd=2, col="blue", col.lab="red", main="Hamlet, Entire Play", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="n",)
axis(1,1:10, labels=names(head(freq, 10)))

