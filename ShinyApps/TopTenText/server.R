function(input, output, session) {
  # Define a reactive expression for the document term matrix
  terms <- reactive({
    # Change when the "update" button is pressed...
    input$update
    # ...but not for anything else
    isolate({
      withProgress({
        setProgress(message = "Processing corpus...")
        getTermMatrix(input$selection)
      })
    })
  })
  
  terms2 <- reactive({
    # Change when the "update" button is pressed...
    input$update
    # ...but not for anything else
    isolate({
      withProgress({
        setProgress(message = "Processing corpus...")
        getTermMatrix(input$selection2)
      })
    })
  })
  
  # Make the wordcloud drawing predictable during a session
  plot_rep <- repeatable(plot)
  
  output$plot1 <- renderPlot({
    v <- terms()
    title <- paste(input$selection, ", Entire Play")
    plot_rep(head(v, 10), type="b", lwd=2, col="blue", col.lab="red", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="n")
    axis(1,1:10, labels=names(head(v, 10)))
  }, height = 400)
  
  output$plot2 <- renderPlot({
    v2 <- terms2()
    title <- paste(input$selection2, ", Entire Play")
    plot_rep(head(v2, 10), type="b", lwd=2, col="blue", col.lab="red", xlab="Top Ten Words", ylab="Number of Occurences", xaxt="n")
    axis(1,1:10, labels=names(head(v2, 10)))
  }, height = 400)
}