#Wordcloud of Top 75 Words in Hamlet

#Set the working directory
setwd("/N/home/c/y/cyberdh/Karst/Text-Analysis/")

#Call libraries used in the script
library(wordcloud)
library(tm)

#Create a corpus -- this creates a wordcloud of the entire Shakesperean corpus
#corpus <- Corpus(DirSource("data/shakespeareFolger"))
# Hamlet Only
text_raw<-scan("data/shakespeareFolger/Hamlet.txt", what="character", sep="\n")

#Create corpus from Hamlet only 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
#To change the stopword list, use other dictionaries available with the tm package
#Add early modern stopwords by u adding "myStopWords
myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
corpus <- tm_map(corpus, removeWords, c(stopwords("english"), myStopWords))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, PlainTextDocument)

wordcloud(corpus,random.order=FALSE,scale=c(4,1),rot.per=0,
          max.words=75,colors=brewer.pal(8, "Dark2"))
