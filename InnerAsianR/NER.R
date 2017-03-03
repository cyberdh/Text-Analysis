library(NLP)
library(openNLP)
library(magrittr)

setwd("~/Desktop/InnerAsianR")
#Read the text in as a simple character vector
autobio <- readLines("Lhasa.txt")
autobio <- paste(autobio, collapse = " ")

#NLP requires us to convert our autobio variable to a string
autobio <- as.String(autobio)
