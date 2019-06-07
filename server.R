library(shiny)
library(tidyverse)
library(shinyWidgets)
library(shinythemes)
library(shinyjs)
library(readxl)
library(shinyalert)
library(reshape)

setwd('/Users/gather3/Documents/Sanitation-Hub')
source('server_modules.R')
options(shiny.maxRequestSize=30*1024^2) 
setwd('/Users/gather3/Documents/General Coding/Database')

server <- function(input, output, session) {
  
  
  # data <- input$csv
  

  selected <- reactiveVal(0)
  
  observeEvent(input$csv,{
    selected(-1)
  })
  
  observeEvent(input$loadDB,{
    selected(1)
  })
  
  data <- reactive({
    
    if(selected() == -1){
      loadFile(input$csv)
    }else if(selected() == 1){
      loadFromDB()
    }
    
  })
  
  
  observeEvent(input$loadDB, {
    if(!is.data.frame(data())){
      shinyalert("Oops!", "Something went wrong", type = "error")
    } else{
      shinyalert("Yes!", "Database loaded succesfully", type = "success")
    }
    
  } )
  
  
  
  output$data_structure <- renderText( {
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    })
  
  output$data_stats <- renderPrint( {
    
    tryCatch(summaryText(data()), error = function(e) {
      
      print("No file selected! Please insert one file on the main page!")
      
    } )
    
    
  })
  
  output$tot <- renderPlot( {
    
    if(is.data.frame(data())){
      
      tryCatch({
      df <- data()
    
      df <- df %>% group_by(type_of_toilet) %>% summarise_if(is.numeric, mean, na.rm = T) %>% ungroup() %>% arrange(desc(number_users))
    
      ggplot(data = df, aes(x = reorder(type_of_toilet, number_users), y = number_users, fill = type_of_toilet)) + 
        geom_col() +
        coord_flip() +
        labs(title = 'Type of Toilet vs Number of users', 
             y = 'Number of Users',
             x = element_blank(),
             fill = 'Type of Toilet') +
        theme_minimal() +
        theme(plot.title = element_text( face = 'bold', size = 26, hjust = 0.5, vjust = 0.3, colour = '#B10048'))
      }, warning = function(w) {
        
        ggplot() + geom_col() +
          labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
        
      }, error = function(e){
        
        ggplot() + geom_col() +
          labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
        
      })
  
    }
      
  } )
  
  output$tot2 <- renderPlotly( {
    
    if(is.data.frame(data())){
      
      tryCatch({
        df <- data()
        
        df <- df %>% group_by(type_of_toilet) %>% summarise_if(is.numeric, mean, na.rm = T) %>% ungroup() %>% arrange(desc(number_users))
        
        plot_ly(df, labels = ~type_of_toilet, values = ~number_users, type = 'pie') %>%
          layout(title = 'People using each type of toilet',
                 xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                 yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
        
        }, warning = function(w) {
          
          ggplot() + geom_col() +
            labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
          
        }, error = function(e){
          
          ggplot() + geom_col() +
            labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
          
      })
      
    }
    
  } )
  
  output$Fill <- renderLeaflet({
    
    if(is.data.frame(data())){
      
      tryCatch({
        
      df <- data() %>% filter(!is.na(latitude) & !is.na(longitude) & !is.na(fill_level))
      
      new_fill <- factor(data()$fill_level, levels = c("Full","Almost full", "Half-full", "Almost empty","Empty"))
          
      pal_fill <- colorFactor("Set1", domain = new_fill, ordered = F)
      
      leaflet(data = df) %>% addProviderTiles(provider = providers$OpenStreetMap) %>% 
        addCircleMarkers(lng = ~longitude, lat = ~latitude, color = ~pal_fill(data()$fill_level),
                         clusterOptions = markerClusterOptions(color = 'black', maxClusterRadius = 100)) %>% 
        addLegend("bottomright", pal = pal_fill, 
                  values = ~new_fill,
                  title = "Fill Level")
      
      }, warning = function(w) {
        ggplot() + geom_col() +
          labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
      }, error = function(e){
        
        ggplot() + geom_col() +
          labs(title = "Your dataset is not like the model, go back to the main menu and follow the guide")
        
      })
    }
    
  })

}