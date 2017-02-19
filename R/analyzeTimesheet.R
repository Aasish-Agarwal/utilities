library(dplyr)
library(googlesheets)
library(stringr)
library(ggplot2)
library(reshape2)
library(scales)
library(ggthemes)


usedPackages <-installed.packages()[,3][c("dplyr", "googlesheets", "stringr",  "ggplot2", "reshape2", "scales", "ggthemes")]
print(usedPackages)

gs_gap()
gap <- gs_title("KnR - Coverage")
data <- gs_read(gap, ws = "Form Responses 1", range = cell_cols(1:91), col_names=TRUE)


mdata <- melt(data, id=c("Timestamp","Email Address"))
colnames(mdata)[2] <- "Email.Address"

mdata1 <- mdata %>% 
  filter( value == "Yes" ) %>%
    group_by(Email.Address, variable) %>% 
      summarize(mindate = min(Timestamp))


mdata2 <- mdata1 %>%
  group_by(Email.Address, mindate) %>%
    summarize(count = n()) %>%
      mutate( growth = cumsum(count))

exercise_map <- dcast(mdata1, variable ~ Email.Address, value.var = "mindate")
gap_reportbook <- gs_title("Pair Programming ITS")
gs_edit_cells( gap_reportbook, ws = "Coverage", input = exercise_map)


gs_edit_cells( gap_reportbook, ws = "Progress", input = mdata2)


## Code tested with
##  dplyr 0.5.0 
##  googlesheets 0.2.1
##  stringr 1.1.0
##  ggplot2 2.1.0
##  reshape2  1.4.2
##  scales  0.3.0
##  ggthemes  3.2.0
