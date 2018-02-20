#Top Ten Words in Hamlet, Curated Stopwords Removed
#Call libraries used in the script
#Set the working directory
setwd("~/Text-Analysis/")
options(mc.cores = 1)
#Call libraries used in the script
library(tm)


#Read in the text 
text_raw<-scan("data/shakespeareFolger/Hamlet.txt", what="character", sep="\n")

#Create a corpus 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords
myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("english"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
#corpus <- tm_map(corpus, PlainTextDocument)

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)

#Remix ideas: 1) Play around with the number of word on the chart by changing it from "10"
# 2) Don't forget the adjust your plot's title if you have changed the input text
# 3) Look the frequency of all the words in the corpus by typing "freq" into the console
barplot(head(freq, 10), ylim=c(0,250), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen"), col.lab="red",
     main="Hamlet, Entire Play", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="s")





