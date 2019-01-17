#Set the working directory
setwd("~/Text-Analysis/")


library(NLP)
library(tm)
library(ggplot2)
library(ggTimeSeries)


#unzip file
#zipF<- "data/twitter/neverAgain.csv.zip"
#outDir<-"data/twitter"
#unzip(zipF,exdir=outDir)


#load file with saved tweets
tweets <- read.csv("data/twitter/parkland/neverAgain.csv", header = T)

corpus <- iconv(tweets$text, to = "utf-8")
corpus <- VCorpus(VectorSource(corpus))


corpus <- tm_map(corpus, content_transformer(function(x) iconv(x, "ASCII", "UTF-8", sub="")))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, stripWhitespace)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
corpus <- tm_map(corpus, content_transformer(removeURL))
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"),'amp','rt', 'dont'))


#Chunk the tweets
chunk.size <- 1000
x <- seq_along(corpus)
text.chunks <- split(corpus, ceiling(x/chunk.size))


#Convert the corpus back to a SimpleCorpus or Corpus object
corpus.chunk <- VCorpus(VectorSource(text.chunks))


#Create matrix using DocumentTermMatrix function and saving it as "dtm"
dtm <- DocumentTermMatrix(corpus.chunk)

# Create a data frame
DF <- data.frame(as.table(dtm), stringsAsFactors = FALSE)
df <- DF[ which(DF$Terms=='nra'|DF$Terms=='gop'|DF$Terms=='parkland'|DF$Terms=='trump'), ]
Tweets <- df$Docs
Frequency <- df$Freq
Terms <- df$Terms


# Plot and print the steamgraph
options(repr.plot.width=12, repr.plot.height=4)
p <- ggplot(df, aes(x=Tweets, y=Frequency, group=Terms, fill=Terms)) +
  stat_steamgraph() +
  theme(axis.text.x=element_text(angle = 45, hjust = 1)) +
  scale_x_discrete(drop=FALSE) +
  scale_fill_brewer(palette = "Dark2") +
  xlab("Tweets in segments of 1000") +
  ggtitle("Streamgraph of 4 words used with twitter #neveragain for 1 week after Parkland shooting")
ggsave(file="~/Text-Analysis/Output/streamgraphNeverAgainTwitter.png", width=8, height=4, dpi=300)
print(p)

