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
<<<<<<< HEAD
<<<<<<< HEAD
=======
    par(mar=c(15, 4.1, 4.1, 2.1))
    title <- paste("Use of '", input$word_choice, "' in Eight Shakespeare Plays")
    mids <- barplot(word.dispersion.df$num,
                    ylab = "Frequency",
                    main = (title), xaxt="n", col = c("lightblue", "mistyrose", "lavender","darkseagreen1","lemonchiffon", "lightsalmon", "plum", "slategray1"))
    axis(1, at=mids, rownames(word.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
    text(mids, 0, word.dispersion.df$num ,cex=1, pos=3, las=2) 
>>>>>>> parent of b96c90d... resolving conflicts (hopefully)

    if (input$word_choice == "love") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(love.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'love' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(love.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, love.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "death") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(death.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'death' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(death.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, death.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "father") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(father.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'father' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(father.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, father.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "power") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(power.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'power' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(power.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, power.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "heaven") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(heaven.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'heaven' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(heaven.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, heaven.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "good") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(good.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'good' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(good.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, good.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "bad") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(bad.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'bad' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(bad.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, bad.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "king") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(king.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'king' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(king.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, king.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "queen") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(queen.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'queen' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon"))
      axis(1, at=mids, rownames(queen.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, queen.dispersion.df$num ,cex=1, pos=3) 
    }

<<<<<<< HEAD
=======
    par(mar=c(15, 4.1, 4.1, 2.1))
    title <- paste("Use of '", input$word_choice, "' in Eight Shakespeare Plays")
    mids <- barplot(word.dispersion.df$num,
                    ylab = "Frequency",
                    main = (title), xaxt="n", col = c("lightblue", "mistyrose", "lavender","darkseagreen1","lemonchiffon", "lightsalmon", "plum", "slategray1"))
    axis(1, at=mids, rownames(word.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
    text(mids, 0, word.dispersion.df$num ,cex=1, pos=3, las=2) 
>>>>>>> parent of b44e3fb... Merge remote-tracking branch 'origin/master'
=======

>>>>>>> parent of b96c90d... resolving conflicts (hopefully)
  }, height=650)
  
  })
}

shinyApp(ui = ui, server = server)
