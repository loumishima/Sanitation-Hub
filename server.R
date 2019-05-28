library(shiny)
library(tidyverse)
library(shinyWidgets)
library(shinythemes)
library(shinyjs)
library(readxl)

source('server_modules.R')
options(shiny.maxRequestSize=30*1024^2) 
setwd('/Users/gather3/Documents/General Coding/Database')

server <- function(input, output, session) {
  
  
  # data <- input$csv
  
  data <- reactive({
    input$csv
  })
  
  
  output$data_structure <- renderText( {
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    })
  
  output$data_stats <- renderPrint( {
    if(is.null(data())){
      'No data has been loaded yet!'
    } else if(grepl('csv', data()$name)){
      infile <- read_csv(data()$datapath, na = '--')
      summary(infile, comp.str = "\n")
    } else {
      infile <- read_excel(path = data()$datapath)
      summary(infile, comp.str = "\n")
      
    }

  })
  

}