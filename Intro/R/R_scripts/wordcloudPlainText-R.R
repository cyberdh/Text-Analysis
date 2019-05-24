#Wordcloud of Top 75 Words in Star Trek: The Next Generation

#Set the working directory
setwd("~/Text-Analysis/")

#Call libraries used in the script
library(wordcloud)
library(tm)

#Create a corpus -- this creates a wordcloud of the entire STNG series
corpus <- VCorpus(DirSource("data/StarTrekNextGenClean/series"))
# A single episode only
#text_raw<-scan("data/StarTrekNextGenClean/series/277.txt", what="character", sep="\n")

#Create corpus from single episode 
#corpus <- VCorpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by adding "myStopWords"
#myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"), 'yes', 'just', 'good'))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)


wordcloud(corpus,random.order=FALSE,scale=c(4,1),rot.per=0,
          max.words=75,colors=brewer.pal(8, "Dark2"))

