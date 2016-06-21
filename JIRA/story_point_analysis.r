library(httr)
library(dplyr)



from_jira_resp_to_history <- function(rawdata) 
{
  resultset <- data.frame()
  
  histories <- rawdata$changelog$histories
  for(history_item in histories) {
    allowed_fields <- c("Story Points", "Epic Link", "Epic Child")
    #item <- history_item$items[[1]];
  
    for(item in history_item$items) {
      if ( item$field %in% allowed_fields ) { 
        fromString = item$fromString
        tstr = item$toString
        
        if( is.null(fromString)) {fromString<-""}
        if( is.null(tstr)) {tstr<-""}
        
        resultset <- rbind(resultset, 
                           rbind(c(item$field , fromString , tstr)))
      }
    }
  }
  resultset$issueid <- rep(rawdata$key,nrow(resultset))
  return(resultset)
}



get_issue_history <- function (issue_list) {
  issue_summary = data.frame()
  for(issue in issue_list){
    issue_url <- paste("https://jira.iontrading.com/rest/api/2/issue/",issue,  "?expand=changelog", sep="")
    var <- GET(issue_url, authenticate('a.agarwal','Khejas'),verbose())
    issue_summary <- rbind(issue_summary,from_jira_resp_to_history(content(var)))
  }
  names(issue_summary) <- c('field','from_string','to_string','id')
  return (issue_summary)
}

# Fetch the list of items to retrieve history
# Get the history of those items
# Keep updating the history, till history of all linked items is not extracted
get_issue_history_recursive <- function (issue_list) {
  
  issue_summary <- get_issue_history( issue_list = all_issues)
  

  repeat{
    all_childs <- issue_summary %>% tbl_df() %>% filter(field %in% c('Epic Child','Epic Link') ,  (to_string != '')) %>% select(to_string) %>% unique() 
    all_childs <- all_childs %>% filter(!(to_string %in% issue_summary$id))
    if( nrow(all_childs) < 1 ){
      break
    }
    issue_summary <- rbind( issue_summary ,
                            get_issue_history( issue_list = all_childs$to_string))
    
  }
    
  return(issue_summary)
}




###########################
# main


all_issues <- c('IONPIVOT-2711',
                'IONPIVOT-2888')

issue_summary <- get_issue_history_recursive(issue_list = all_issues)


size_variation <- issue_summary %>% filter(field == "Story Points") %>% group_by(id) %>% 
  summarize( start_size <- min(as.numeric(as.character(from_string)), na.rm = TRUE) , 
             end_size <- last(to_string))

names(size_variation) <- c('id','initial_size','final_size')

size_variation <- size_variation  %>%
  mutate(initial_size = ifelse( is.infinite(initial_size), as.numeric(as.character(final_size)), initial_size))


epic <- issue_summary %>% filter(field == 'Epic Child' , to_string != '' ) %>%  
  mutate (child_id = to_string) %>% select(id,child_id) %>%  unique()

epic <- merge(epic, size_variation, by.x = "child_id", by.y = "id", all.x=TRUE) 

epic  <- epic %>% mutate ( final_size = as.numeric(as.character(final_size))) 

epic <- epic %>% mutate(isclildanepic = (child_id %in% id) , notsized = ifelse( is.na(final_size), T, F))


epic_sizes <- epic %>% group_by(id) %>% summarize(num_childs = n() , total_size = sum(final_size,na.rm = T) , 
                                    unsized = sum(notsized) , epicchilds = sum(isclildanepic))

  
get_epic_size_recursive <- function (issue) {
  all_childs <- c()
  v1 <- c(issue)
  repeat{
    # Extract the list of childs of the given list which are an epic in themselves 
    ndf <- epic %>% filter( epic$id %in% v1 , isclildanepic == T)
    v1 <- as.character(ndf$child_id)
  
    # If the list is empty break the loop
    if ( length(v1) < 1 ) {
      break
    }
    
    # Else add the new list of chidren to the list of epic childs
    all_childs <- append(all_childs, v1)
    # Use this list of epic childs to fetch the next list of children
  }
  
  ndf <- epic_sizes %>% filter(id %in% all_childs) %>% summarize(epic_child_size = sum(total_size))
  ndf$id <- rep(issue,nrow(ndf))
  return(ndf)
}

epic_clild_size_df <- data.frame()
for (issue in unique(as.character(filter( epic, isclildanepic == T)$id))){
  epic_clild_size_df <- rbind(epic_clild_size_df,get_epic_size_recursive(issue))
}



