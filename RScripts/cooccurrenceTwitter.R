#Call libraries used in the script 
library(tm)
library(RColorBrewer)
library(topicmodels)
library(plyr)
library(twitteR)
library(dplyr)
library(tidytext)
library(fuzzyjoin)
library(SnowballC)
library(stringr)



#Set the working directory
setwd("~/Text-Analysis/")

#unzip file
zipF<- "data/twitter/neverAgain.csv.zip"
outDir<-"data/twitter"
unzip(zipF,exdir=outDir)

#load file with saved tweets
tweets <- read.csv("data/twitter/neverAgainSnippet.csv", header = T)
myStopWords <- c("rt", "amp")

corpus <- iconv(tweets$text, to = "utf-8")
corpus <- Corpus(VectorSource(corpus))

#clean corpus
mycorpus <- tolower(corpus)
removeChars <- function(x) iconv(x, "ASCII", "UTF-8", sub="")
mycorpus <- removeChars(mycorpus)
mycorpus <- removeNumbers(mycorpus)
mycorpus <- removePunctuation(mycorpus)
mycorpus <- stripWhitespace(mycorpus)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
mycorpus <- removeURL(mycorpus)
mycorpus <- removeWords(mycorpus, myStopWords)

#tokenize the corpus into a data.frame where each row is one word
all_words <- data_frame(text = mycorpus) %>%
  unnest_tokens(word, text) %>%
  #add a position column
  mutate(position = row_number()) %>%
  #remove regular english stopwords from the tm package
  filter(!word %in% tm::stopwords("en"))

nearby_words <- all_words %>%
  filter(word == "neveragain") %>%
  #filter(word %in% c("father", "good")) %>%
  select(focus_term = word, focus_position = position) %>%
  difference_inner_join(all_words, by = c(focus_position = "position"), max_dist = 5) %>%
  mutate(distance = abs(focus_position - position))

words_summarized <- nearby_words %>%
  group_by(word) %>%
  #group_by(focus_term, word) %>%
  summarize(number = n(),
            maximum_distance = max(distance),
            minimum_distance = min(distance),
            average_distance = mean(distance)) %>%
  arrange(desc(number))
print(head(words_summarized, 12))

#plot average_distance to barplot
names <- head(words_summarized$word, 11)
average <- head(words_summarized$average_distance, 11)

par(mar=c(8,5,3,1))

p <- barplot(average, ylim=c(0,5), col=c("red3", "orange3","yellow3","green3","blue3","darkorchid3","darkred", "darkorange", "gold", "darkgreen", "navyblue"), col.lab="black",
        main="Co-occurrence of Words", xlab="Top Ten Occurrences", ylab="Average Distance", xaxt="n")
axis(1, at=p, labels=FALSE)
text(p, par("usr")[3], srt=45, adj=c(1.1,1.5), xpd = TRUE, labels=names, cex=.9)
print(p)

#Save table to csv file for more detailed data 
write.csv(words_summarized, file = "ChooseAnyNameYouWant.csv")
#Much of this code was derived from David Robinson on stackoverflow who created the tidytext and fuzzyjoin packages in R.
