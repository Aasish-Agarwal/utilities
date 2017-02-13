library(dplyr)
library(googlesheets)
library(stringr)
library(ggplot2)
library(reshape2)
library(scales)
library(ggthemes)

gs_gap()
gap <- gs_title("KnR - Coverage")
data <- gap %>% gs_read(ws = "Form Responses 1", range = cell_cols(1:91), col_names=TRUE)


mdata <- melt(data, id=c("Timestamp","Email.Address"))

mdata1 <- mdata %>% 
  filter( value == "Yes" ) %>%
    group_by(Email.Address, variable) %>% 
      summarize(mindate = min(Timestamp))


mdata2 <- mdata1 %>%
  group_by(Email.Address, mindate) %>%
    summarize(count = n()) %>%
      mutate( growth = cumsum(count))

