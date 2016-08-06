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
corpus <- tm_map(corpus, PlainTextDocument)

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)


plot(head(freq, 10), type="b", lwd=2, col="blue", col.lab="red",
     main="Hamlet, Entire Play", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="n",)
axis(1,1:10, labels=names(head(freq, 10)))

