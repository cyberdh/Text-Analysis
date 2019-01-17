#Top Ten Words in an Episode of Star Trek: The Next Generation, Curated Stopwords Removed
#Call libraries used in the script
#Set the working directory
setwd("~/Text-Analysis/")
options(mc.cores = 1)
#Call libraries used in the script
library(tm)

#Creat a corpus -- this creates a corpus of the entire STNG series
corpus <- VCorpus(DirSource("data/StarTrekNextGenClean/series"))

#Read in the text of a single episode 
#text_raw<-scan("data/StarTrekNextGenClean/series/277.txt", what="character", sep="\n")

#Create a corpus from single episode 
#corpus <- VCorpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tolower(corpus)
#Add early modern stopwords
#myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- removeWords(corpus, c(stopwords("SMART"), "just", "ill"))
corpus <- removePunctuation(corpus)
corpus <- stripWhitespace(corpus)

corpus <- VCorpus(VectorSource(corpus))

dtm <- DocumentTermMatrix(corpus)
freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)

#Convert to data frame (helps make plot labeling easier)
freqDF <- as.data.frame.character(freq)

head(freqDF)

freqDF$words <- rownames(freqDF)

labNames <- head(freqDF$words, 10)



#Remix ideas: 1) Play around with the number of word on the chart by changing it from "10"
# 2) Don't forget the adjust your plot's title if you have changed the input text
# 3) Look the frequency of all the words in the corpus by typing "freq" into the console
par(mar=c(15,4,4,0))
x <- barplot(head(freq, 10), ylim=c(0,5000), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen"), col.main="Gold", col.lab="red",
             main="Star Trek: The Next Generation", xlab="", ylab="Number of Occurences", xaxt="n")
axis(2, at=x, labels=TRUE)
axis(2, col="gray27", col.axis="gray27", col.ticks="gray27",labels=TRUE)
text(x, par("usr")[3], srt=45, adj=c(1.1,1.5),xpd = TRUE, labels = labNames, cex=.9, col="gray27", col.axis="gray27")
title(xlab='Top Ten Words', line=5, col.lab="red")
print(x)           




