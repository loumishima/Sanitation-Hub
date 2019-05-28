library(tidyverse)
library(shiny)
library(RPostgreSQL)
library(data.table)


connect <- function(drv = "PostgreSQL", dbname = 'teste123', host = 'localhost', login = 'gather3', pwd = 'Toilet2019'){
  
  con <- dbConnect(drv, dbname = dbname,
                   host = host, port = 5432,
                   user = login, password = pwd)
  return(con)
}

setwd('/Users/gather3/Documents/General Coding/Web Scraping')

nfl <- read.csv('nfl.csv')

#Processing step inside here

nfl <- nfl %>% select(-X)

con <- connect()


#Writing on the DB
dbWriteTable(con, 'nfl_passing', nfl, row.names = F, append = TRUE )


# Loading from the DB
x <- dbGetQuery(con, 'Select * from nfl_passing', stringsAsFactors = FALSE)

# The df must have the same name as the original db!.