#Wordcloud of Top 75 Words in Hamlet

#Set the working directory
setwd("~/Desktop/R/Text_Analysis/data/shakespeareFolger")

#Call libraries used in the script
library(wordcloud)
library(tm)

#Create a corpus -- this creates a wordcloud of the entire Shakesperean corpus
# corpus <- Corpus(DirSource("shakespeareFolger"))
# Hamlet Only
text_raw<-scan("Hamlet.txt", what="character", sep="\n")

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords
myStopWords <- scan("~/Desktop/R/Text_Analysis/data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("SMART"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, PlainTextDocument)

wordcloud(corpus,random.order=FALSE,scale=c(3,.5),rot.per=0,
          max.words=55,colors=brewer.pal(8, "Dark2"))