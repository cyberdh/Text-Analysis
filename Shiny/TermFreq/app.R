library(ggplot2)


ui <- fluidPage(
  titlePanel("Frequency of Terms Across a Corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows how frequent certain words appear in each text throughout a section of the Shakespeare Drama Corpus."),
      selectInput(inputId = "word_choice",
                  label = "Choose a word:",
                  choices = c("love", "death", "father", "power", "heaven", "good", "bad", "king", "queen"),
                  selected = "love")
      
    ),
    
    mainPanel(
      plotOutput("plot")
    )
  )
  
)

server <- function(input, output) {
  observe({
   # setwd("~/Documents/IU/CyberDH/Text_Analysis/data/") #Set directory path for your environment 
    library(ggplot2)
   # input.dir <- "shakesFreqs"
   files.v <- dir(pattern= "\\.txt$")

    find.dispersion <- function(files.v){
      text.word.vector.l <- list()
      #loop over the files
      for(i in 1:length(files.v)) {
        text.v <- scan(files.v[i], what="character", sep="\n")
      
      
      text.lower.v<-tolower(text.v)
      text.words.v<-strsplit(text.lower.v, "\\W")
      text.word.v<-unlist(text.words.v)
      not.blanks.v <- which(text.word.v != "")
      text.word.v <- text.word.v[not.blanks.v]
      
      text.position.v <- seq(1:length(text.word.v))
      love.v <- which(text.word.v == input$word_choice)
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
  word.dispersion <- find.dispersion(files.v)
  
  class(word.dispersion)
  
  word.dispersion.df <- do.call(rbind.data.frame, word.dispersion)
  colnames(word.dispersion.df)[1] <- "num"
  rownames(word.dispersion.df)
  
  
  
  
  output$plot <- renderPlot({
    par(mar=c(15, 4.1, 4.1, 2.1))
    title <- paste("Use of '", input$word_choice, "' in Five Shakespeare Plays")
    mids <- barplot(word.dispersion.df$num,
                    ylab = "Frequency",
                    main = (title), xaxt="n", col = c("lightblue", "mistyrose", "lavender","darkseagreen1","lemonchiffon", "lightsalmon", "plum", "slategray1"))
    axis(1, at=mids, rownames(word.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
    text(mids, 0, word.dispersion.df$num ,cex=1, pos=3, las=2) 
  }, height=650)
  
  })
}

shinyApp(ui = ui, server = server)
