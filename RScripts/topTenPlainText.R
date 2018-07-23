#Top Ten Words in an Episode of Star Trek: The Next Generation, Curated Stopwords Removed
#Call libraries used in the script
#Set the working directory
setwd("~/Text-Analysis/")
options(mc.cores = 1)
#Call libraries used in the script
library(tm)

#Creat a corpus -- this creates a corpus of the entire STNG series
#corpus <- Corpus(DirSource("data/StarTrekNextGenClean/series"))

#Read in the text of a single episode 
text_raw<-scan("data/StarTrekNextGenClean/series/277.txt", what="character", sep="\n")

#Create a corpus from single episode 
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
par(mar=c(15,4,4,0))
barplot(head(freq, 10), ylim=c(0,100), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen"), col.main="Gold", col.lab="red", col.axis="gray28", las=2,
     main="Star Trek: The Next Generation, Final Episode", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="s")





