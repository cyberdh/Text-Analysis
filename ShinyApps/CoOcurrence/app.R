ui <- fluidPage(
  titlePanel("Co-Occurrence of Terms Across a Corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive rendering shows the percentage of certain words which appear near the target word throughout the Shakespeare Drama Corpus."),
      selectInput(inputId = "word_choice",
                  label = "Choose a the target word:",
                  choices = c("love", "death", "father", "power", "heaven", "good", "bad", "king", "queen"),
                  selected = "love")
      
    ),
    mainPanel(
      verbatimTextOutput("cotext")
    )
    )
  )
  


server <- function(input, output) {
  observe({
    #setwd("~/Documents/IU/CyberDH/Text_Analysis/data/") #Set directory path for your environment 
    library(tm)
    library(RWeka)
    
    #Set the working directory
    #setwd("~/Documents/IU/CyberDH/Text_Analysis/data/")
    
    #Read in the text 
    #text_raw<-scan("Hamlet.txt", what="character", sep="\n")
    
    #Create a corpus 
    corpus <- Corpus(DirSource("shakespeareFolger"))
    
    #Clean the corpus
    corpus <- tm_map(corpus, content_transformer(tolower))
    corpus <- tm_map(corpus, removeWords, stopwords("SMART"))
    corpus <- tm_map(corpus, removeWords, c("tis", "hath"))
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, stripWhitespace)
    #corpus <- tm_map(corpus, PlainTextDocument)
    
    dtm <- DocumentTermMatrix(corpus)
    freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)
    
    
    output$cotext  <- renderPrint({
      findAssocs(dtm, input$word_choice, .6)
    })
    
  })
}

shinyApp(ui = ui, server = server)
