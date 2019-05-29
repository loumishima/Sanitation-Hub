library(tidyverse)
library(shiny)
library(RPostgreSQL)
library(data.table)
library(readxl)

# Database connection ----
connect <- function(drv = "PostgreSQL", dbname = 'teste123', host = 'localhost', login = 'gather3', pwd = 'Toilet2019'){
  
  con <- dbConnect(drv, dbname = dbname,
                   host = host, port = 5432,
                   user = login, password = pwd)
  return(con)
}

# Reading Files ----
setwd('/Users/gather3/Documents/General Coding/Database')

Kanyama <- read_csv("Kanyama_to_plot.csv")
Mathare <- read_csv("mathare2017-2.csv")
Dhaka <- read_csv("indicatorsDataBGD.csv")

# Using the Kanyama data as the golden model
# Mathare part ----
Mathare <- Mathare %>% select(-c(the_geom,
                                 provider,
                                 cartodb_id,
                                 solidwaste,
                                 gender,
                                 soap,
                                 opennight,
                                 handwash,
                                 menstrual,
                                 ashsawdust,
                                 water,
                                 users,
                                 cost,
                                 connection_type,
                                 stalls,
                                 location,
                                 area,
                                 name,
                                 waypoint))
Mathare <- Mathare %>% mutate(City = 'Mathare')

Mathare <- Mathare %>% select(City,Latitude = st_x, Longitude = st_y, everything())

# Kanyama part ----

Kanyama <- Kanyama %>% mutate(City = 'Kanyama')

Kanyama <- Kanyama %>% select(City, Latitude = X1.9..latitude., Longitude = X1.9..longitude.,
                              Is.the.toilet.easily.accessible.to.the.following.people...Persons.with.dissability,
                              people.using.toilet,
                              Perception.of.the.fill.level,
                              Water.source..fetch.,
                              Interface.Layout,
                              Is.washing.hand.basin.present.)


# Dhaka part ----

Dhaka <- Dhaka %>% mutate(Fill.level = NA_character_, jmpHand2 = if_else(jmpHand2 > 0, 'yes', 'no'))
Dhaka <- Dhaka %>% select(City = country, Latitude = latitude, Longitude = longitude,
                          nMobility, nMembers, Fill.level,
                          waterSource,
                          san3,
                          jmpHand2)


# Making a common name to the columns ----

col.names <- c('city', 'latitude', 'longitude', 'mobility', 'number_users', 'fill_level',
               'water_source', 'type_of_toilet', 'washing_basin')

names(Dhaka) <- col.names
names(Kanyama) <- col.names
names(Mathare) <- col.names

connected <- rbind(Mathare,Dhaka, Kanyama)

connected <- connected %>% mutate(mobility = case_when(mobility == "yes" | mobility == "1" | mobility == TRUE ~ TRUE,
                                                       mobility == "no" | mobility == "0" | mobility == FALSE ~ FALSE),
                                  washing_basin = if_else(toupper(washing_basin) == 'YES', TRUE, FALSE),
                                  fill_level = case_when(fill_level == '100 monthly' ~ 'Full',
                                                         fill_level == 'half full' ~ 'Half-full',
                                                         fill_level == 'mostly empty' | fill_level == 'completely empty' ~ 'Almost empty',
                                                         fill_level == 'not applicable' | fill_level == 'unknown' | fill_level == 'no' ~ NA_character_,
                                                         TRUE ~ fill_level))


con <- connect()

#Writing on the DB
dbWriteTable(con, 'sanitation', connected, row.names = F, append = TRUE )

x <- dbGetQuery(con, 'Select * from sanitation', stringsAsFactors = FALSE)

dbDisconnect(con)








