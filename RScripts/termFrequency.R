setwd("~/Desktop/R/") #Set directory path for your environment 
library(ggplot2)
input.dir <- "Text_Analysis/data/shakesFreqs"
files.v <- dir(input.dir, "\\.txt$")


find.dispersion <- function(files.v, input.dir){
  text.word.vector.l <- list()
  #loop over the files
  for(i in 1:length(files.v)) {
    text.v <- scan(paste(input.dir, files.v[i], sep="/"), what="character", sep="\n")
    
    
    text.lower.v<-tolower(text.v)
    text.words.v<-strsplit(text.lower.v, "\\W")
    text.word.v<-unlist(text.words.v)
    not.blanks.v <- which(text.word.v != "")
    text.word.v <- text.word.v[not.blanks.v]
    
    text.position.v <- seq(1:length(text.word.v))
    love.v <- which(text.word.v == "love")
    w.count.v <- rep(NA, length(text.position.v))
    w.count.v[love.v] <- 1
    sum.occurences <- sum(w.count.v, NA, na.rm = TRUE)
    
    
    
    #use the index id from the viles.v vector as the "name" in the list
    text.word.vector.l[[files.v[i]]] <- sum.occurences
  }
  return(text.word.vector.l)
}

show.files <- function(file.name.v){
  for(i in 1:length(file.name.v)){
    cat(i, file.name.v[i], "\n", sep=" ")
  }
}

# run function and store result in list object 
word.dispersion <- find.dispersion(files.v, input.dir)

class(word.dispersion)

word.dispersion.df <- do.call(rbind.data.frame, word.dispersion)
colnames(word.dispersion.df)[1] <- "num"
colnames(word.dispersion.df)[0] <- "play" #this line also does nothing!

barplot(word.dispersion.df$num,
        xlab = "Plays", ylab = "Frequency",
        main = "Use of 'love' in Five Shakespeare Plays")
axis(1,1:5, labels=names(word.dispersion.df[1]) # This line doesn't work!!!


