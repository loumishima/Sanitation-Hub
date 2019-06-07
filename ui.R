library(shiny)
library(dplyr)
library(shinyWidgets)
library(shinythemes)
library(shinyjs)
library(shinyalert)
library(plotly)

setwd('/Users/gather3/Documents/Sanitation-Hub')
source('ui_modules.R')

setwd('/Users/gather3/Documents/General Coding/Database')

ui <- tagList(
  useShinyalert(),
  tags$head(tags$script(type="text/javascript", src = "code.js")),
  navbarPage(title = 'Sanitation Hub - Data Colection', id = 'nav', theme = 'style.css',
             
             tabPanel(title = 'Data colection', id = 'colection', value = 0,
                      
                      fluidRow(
                        column(4, offset = 4,
                               'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                               br(),
                               br(),
                               fileInput('csv', width = '100%',
                                         label = 'Choose the file to update',
                                         buttonLabel = 'Browse',
                                         accept = c("text/csv", ".csv", ".xls", ".xlsx"),
                                         placeholder = 'No file selected'),
                               "Case you want to see our current database, click on the button below",
                               br(),
                               br(),
                               fluidRow(
                                 column( width = 4 , offset = 3, actionButton('loadDB', label = 'Load Database', icon = icon("upload"), width = '200px'))
                               ),
                               br(),
                               br(),
                               "If your file follows all the instructions above, you file may be available to upload on the Gather's Sanitation Hub! Just press the button and the system will make all the verifications to 
                               send you data",
                               br(),
                               br(),
                               fluidRow(
                                column(width = 4, offset = 3, actionButton('Submit',"Send to the database", icon("database"), width = '200px'))
                               )
                              
                             )
                      )
                      
                      
                      ),
             tabPanel(title = 'Data overview', id = 'overview', value = 1,
                      textOutput("data_structure"),
                      br(),
                      verbatimTextOutput("data_stats")
                      ),
             tabPanel(title = 'Data analysis', id = 'analysis', value = 2,
                      tabsetPanel(id = 'analysis-selection', type = 'tabs',
                                  tabPanel('Type of Toilets', plotOutput('tot', height = '600px'),
                                           br(),
                                           br(),
                                           plotlyOutput('tot2', height = '600px')),
                                  tabPanel('Fill Level', leafletOutput('Fill', height = '600px')),
                                  tabPanel('Maps Visualisations', leafletOutput('Map')))
                      )
  )
)