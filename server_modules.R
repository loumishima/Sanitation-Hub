library(shiny)
library(dplyr)
library(leaflet)
library(ggplot2)
library(lubridate)
library(scales)
library(shinyWidgets)
library(shinythemes)
library(shinyjs)
library(RPostgreSQL)
library(pool)


plotProcessing <- function(input, output, session, selection, datasetOne, datasetTwo, attribute = "number.of.cases"){
  
  if(selection == 0){
    result <- datasetOne
    result$date.full <- as.Date(result$date.full)
    result<- filter(result, year(result$date.full) == input$year.selection)
    
  }
  else{
    
    result<- filter(datasetTwo, 
                    datasetTwo$date.full > input$month.selection[1] & Daily.plot$date.full < input$month.selection[2] )
    
    
  }
  
  return(result)
  
  
  
  
}

sliderPlotProcessing <- function(input, output, session, result){
  
  result$date.full <- as.Date(result$date.full)
  result<- filter(result, year(result$date.full) == input$year.selection)
  
  # if(length(levels(factor(result$Transport))) == 3){
  #   colour <- result$Transport
  # }
  
  return(result)
}

dateRangePlotProcessing <- function(input, output, session, result){
  
  result$date.full <- as.Date(result$date.full )
  result<- filter(result, result$date.full > input$month.selection[1] & result$date.full < input$month.selection[2])
  
  return(result)
  
}

disableRadioOptions <- function(input, output, session, values){
  
  observe({
    if(input$tabset == 'General') {
      disable("plot.selection")
    } else {
      enable("plot.selection")
    }
  })
}
  

activateDetailedView <- function(input, output, session, values){
 
   observeEvent(input$detail,{
    values$active = !values$active
    if(values$active == T){
      updateActionButton(session, inputId = "detail", label = "Disable month selection" )
      enable(id = "month.selection")
      disable(id = "year.selection")
      
    } else {
      updateActionButton(session, inputId = "detail", label = "Enable month selection" )
      disable(id = "month.selection")
      enable(id = "year.selection")

    }
    

    
  })
}

refreshButton<- function(input, output, session, values){
  values$active = FALSE
  disable("month.selection")
  enable("year.selection")
  updateActionButton(session, inputId = "detail", label = "Enable month selection" )

}

startSettings <- function(input, output, session, values){
  
  disable("month.selection")
  updateActionButton(session, inputId = "detail", label = "Enable month selection" )
  
}
  

plotSelected <- function(input, output, session){
  
 answer <- reactiveValues()
 
 observe({answer$sel <- input$plot.selection})
  
 return(answer)
}  

loadFile <- function(data) {
  
  if(is.null(data)){
    'No data has been loaded yet!'
  } else if(grepl('csv', data$name)){
    infile <- read_csv(data$datapath, na = '--')
    return(infile)
  } else {
    infile <- read_excel(path = data()$datapath)
    return(infile)
    
  }
}


loadFromDB <- function(drv = "PostgreSQL", dbname = 'teste123', host = 'localhost', login = 'gather3', pwd = 'Toilet2019',
                       database = 'sanitation'){
  
  pool <- dbPool(drv, dbname = dbname,
                 host = host, port = 5432,
                 user = login, password = pwd,
                 idleTimeout = 60)
  
  file <- dbGetQuery(pool, paste('Select * from', database), stringsAsFactors = FALSE)
  
  poolClose(pool)
  
  return(file)
  
}

summaryText <- function(df){
  
  df <- as.data.frame(summary(df))
  
  df <- filter(df, !is.na(Freq)) %>% filter(., !grepl("^(Class|Mode)", Freq))
  
  df <- mutate(df, Var1 = str_extract(Freq, "^.*:"), Var1 = gsub(":", "", Var1)) 
  
  df <- df %>% cast( Var2 ~ Var1, add.missing = T)
  
  df <- mutate(df,index = rownames(df)) %>% select(.,c(index, everything()))
  
  text <- apply(df, 1, function(x) textStructure(x))
  
  return(cat(text))
  
}

textStructure <- function(x){
  
  x <- x[!is.na(x)]
  text <- paste("Position:", x[1] , "\n")
  text <- paste(text, "Column:", x[2], "\n" )
  x <- x[3:length(x)]
  for (variable in x) {
    text<-paste0( text,"\t" , variable , "\n")
  }

  return(text)
}
  