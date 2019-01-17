#Set the working directory
setwd("~/Text-Analysis/")

#load necessary packages
library(NLP)
library(tm)
library(ggplot2)
library(ggTimeSeries)
library(readtext)


#Create a corpus
corpus <- readtext("data/StarTrekNextGenClean/series/277.txt")


#Clean the corpus
corpus <- tolower(corpus)
#To change the stopword list, use other dictionaries available with the tm package
corpus <- removeWords(corpus, stopwords("SMART"))
corpus <- removeNumbers(corpus)
corpus <- removePunctuation(corpus)
corpus <- stripWhitespace(corpus)


x <- unlist(strsplit(corpus, "\\s+"))
text.chunks <- split(x, seq_along(x)%/%250)

#Convert the corpus back to a SimpleCorpus or Corpus object
corpus.chunk <- Corpus(VectorSource(text.chunks))


#Create matrix using DocumentTermMatrix function and saving it as "dtm"
dtm <- DocumentTermMatrix(corpus.chunk)


#Turn document term matrix into a tidy data frame
DF <- data.frame(as.table(dtm), stringsAsFactors = FALSE)
df <- DF[ which(DF$Terms=='captain'|DF$Terms=='time'|DF$Terms=='anomaly'), ]
Chunks <- df$Docs
Frequency <- df$Freq
Terms <- df$Terms
head(df, 10)

#Plot and print streamgraph
options(repr.plot.width=10, repr.plot.height=4)
p <- ggplot(df, aes(x=Chunks, y=Frequency, group=Terms, fill=Terms)) +
  stat_steamgraph() +
  theme(axis.text.x=element_text(angle = 45, hjust = 1)) +
  scale_x_discrete(drop=FALSE) +
  scale_fill_brewer(palette = "Dark2") +
  xlab("Segments of 250 Words") +
  ggtitle("Steamgraph of 3 words in Episode of Star Trek: The Next Generation") +
  ggsave(file="~/Text-Analysis/Output/steamgraphPlainText.png", width=8, height=4, dpi=300)
print(p)

