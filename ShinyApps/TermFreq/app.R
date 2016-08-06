library(ggplot2)
library(shiny)


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
   # setwd("~/Desktop/R/Text_Analysis/data/") #Set directory path for your environment 
    library(ggplot2)
   # input.dir <- "shakesFreqs"
   
  love.dispersion.df <- read.table(file = "loveDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(love.dispersion.df)[1] <- "num"
  
  death.dispersion.df <- read.table(file = "deathDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(death.dispersion.df)[1] <- "num"
  
  father.dispersion.df <- read.table(file = "fatherDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(father.dispersion.df)[1] <- "num"
  
  heaven.dispersion.df <- read.table(file = "heavenDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(heaven.dispersion.df)[1] <- "num"
  
  power.dispersion.df <- read.table(file = "powerDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(power.dispersion.df)[1] <- "num"
  
  good.dispersion.df <- read.table(file = "goodDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(good.dispersion.df)[1] <- "num"
  
  bad.dispersion.df <- read.table(file = "badDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(bad.dispersion.df)[1] <- "num"
  
  king.dispersion.df <- read.table(file = "kingDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(king.dispersion.df)[1] <- "num"
  
  queen.dispersion.df <- read.table(file = "queenDF.csv", row.names = 1, head=TRUE, sep=",")
  colnames(queen.dispersion.df)[1] <- "num"
  
  
  
  
  
  
  output$plot <- renderPlot({
    if (input$word_choice == "love") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(love.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'love' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(love.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, love.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "death") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(death.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'death' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(death.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, death.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "father") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(father.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'father' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(father.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, father.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "power") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(power.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'power' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(power.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, power.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "heaven") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(heaven.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'heaven' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(heaven.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, heaven.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "good") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(good.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'good' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(good.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, good.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "bad") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(bad.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'bad' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(bad.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, bad.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "king") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(king.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'king' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(king.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, king.dispersion.df$num ,cex=1, pos=3) 
    }
    else if (input$word_choice == "queen") {
      par(mar=c(15, 4.1, 4.1, 2.1))
      mids <- barplot(queen.dispersion.df$num,
                      ylab = "Frequency",
                      main = "Use of 'queen' in Eight Shakespeare Plays", xaxt="n", col = c("lightblue", "mistyrose", "lavender","palegreen","lemonchiffon", "coral", "skyblue", "darkolivegreen1"))
      axis(1, at=mids, rownames(queen.dispersion.df), tick=FALSE, xpd = TRUE, las=2)
      text(mids, 0, queen.dispersion.df$num ,cex=1, pos=3) 
    }

  }, height=650)
  
  })
}

shinyApp(ui = ui, server = server)
