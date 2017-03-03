library(NLP)
library(openNLP)
library(magrittr)

setwd("~/Desktop/InnerAsianR")
#Read the text in as a simple character vector
bio <- readLines("WayfarerKendall.txt")
bio <- paste(bio, collapse = " ")

#NLP requires us to convert our text variable to a string
autobio <- as.String(autobio)

#Create annotators using underlyling Java libraries
word_ann <- Maxent_Word_Token_Annotator()
sent_ann <- Maxent_Sent_Token_Annotator()

#Use another constructor function to find locations
location_ann <- Maxent_Entity_Annotator(kind = "location")

#Create a new pipeline list to hold annotators in the order we want to apply them. 
pipeline <- list(sent_ann,
                 word_ann,
                 location_ann)
bio_annotations <- annotate(bio, pipeline)
bio_doc <- AnnotatedPlainTextDocument(bio, bio_annotations)

# Extract entities from an AnnotatedPlainTextDocument
entities <- function(doc, kind) {
  s <- doc$content
  a <- annotations(doc)[[1]]
  if(hasArg(kind)) {
    k <- sapply(a$features, `[[`, "kind")
    if(length(a[k==kind])>0){
      s[a[k == kind]]}
  } else {
    s[a[a$type == "entity"]]
  }
}

locations = entities(bio_doc, kind = "location")
write.csv(locations, "LocationsWayfarer.csv")

library(ggmap)