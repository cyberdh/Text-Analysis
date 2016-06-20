#Top Ten Words in Hamlet, Curated Stopwords Removed

#Set the working directory
#setwd("~/Documents/IU/CyberDH/Text_Analysis/data/shakespeareFolger/")

plays <<- list("Hamlet" = "Hamlet", "King Lear" = "KingLear", "King Richard III" = "KingRichard3", "Macbeth" = "Macbeth", "A Midsummer Night's Dream" = "MidsummerNightsDream", "Othello" = "Othello", "Romeo and Juliet" = "RomeoAndJuliet", "Twelfth Night" = "TwelfthNight")
#Call libraries used in the script
library(tm)
library(memoise)

#Call libraries used in the script
#library(wordcloud)
#library(tm)
#library(Rcolorbrewer)

getTermMatrix <- function(play) {
  # Careful not to let just any name slip in here; a
  # malicious user could manipulate this value.
  if (!(play %in% plays))
    stop("Unknown book")
  
  #Read in the text 
  text_raw<-scan(paste(play, '.txt', sep = "", collapse = NULL), what="character", sep="\n")
  
  #Create a corpus 
  corpus <- Corpus(VectorSource(text_raw))
  
  #Clean the corpus
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removeWords, stopwords("SMART"))
  corpus <- tm_map(corpus, removeWords, c("tis", "hath"))
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, stripWhitespace)
  corpus <- tm_map(corpus, PlainTextDocument)
  
  dtm <- DocumentTermMatrix(corpus)
  sort(colSums(as.matrix(dtm)), decreasing = TRUE)
}
