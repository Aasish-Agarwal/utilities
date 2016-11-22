# Objective
# We need a mechanism to extract the team name and sprint number from a sprint object  

getTeamAndSprint <- function (sprintsObjectString) {
  sprintList <- strsplit(sprintsObjectString, ",")
  sprintNameList <- grep("name=", sprintList[[1]], value = T)
  
  teamSprintMatrix <- sapply(sprintNameList,extractTeamAndSprintFromString)
  teamSprintDF <- convertMatrixToTeamSprintDataFrame(teamSprintMatrix)
  return(teamSprintDF)
}

extractTeamAndSprintFromString <- function( inStr ) {
  sprintFullName <- strsplit(inStr ,"=")[[1]][2]
  teamSprintVector <- strsplit(stringr::str_trim(sprintFullName),"\\s+")[[1]]
  
  team <- extractTeamName(teamSprintVector)
  sprint <- extractSprintNumber(teamSprintVector)
  
  return (c(team,sprint))
}

extractTeamName <- function( teamSprintVector ) {
  return(paste(head(teamSprintVector,-2), sep="", collapse=" "))
}

extractSprintNumber <- function( teamSprintVector ) {
  return(tail(teamSprintVector,1))
}

convertMatrixToTeamSprintDataFrame <- function ( teamSprintMatrix ) {
  teamSprintMatrix <- as.data.frame(t(as.data.frame(teamSprintMatrix)))
  row.names(teamSprintMatrix) <- NULL
  names(teamSprintMatrix) <- c("team", "sprint")
  return(teamSprintMatrix)
}
##################################################################################
##  Acceptance Tests Definition
# Following acceptance tests must be successful after this function is implemented

testHelperExtractTeamAndSprint <- function ( issueSprintsString , expectedDF , testName ) {
  actualDF <- getTeamAndSprint(issueSprintsString)
  actualDF <- data.frame(lapply(actualDF,as.character),stringsAsFactors = F)
  expectedDF <- data.frame(lapply(expectedDF,as.character),stringsAsFactors = F)

    if ( identical(actualDF,expectedDF) ) { 
    print ( paste( testName , ": OK"))
  } else {
    print ( paste( testName , ": FAIL"))
  }
}

MultipleSprintsCanBeExtracted <- function ( callstack=sys.calls() ) {
  functionNameSelf <- callstack[[6]]

  issueSprints <- "c(\"com.atlassian.greenhopper.service.sprint.Sprint@50eaa052[rapidViewId=11,state=CLOSED,name=ARCADE Sprint 113,startDate=2016-10-06T14:40:52.687+01:00,endDate=2016-10-20T14:40:00.000+01:00,completeDate=2016-10-21T06:32:06.424+01:00,sequence=3713,id=3713]\", \"com.atlassian.greenhopper.service.sprint.Sprint@2f7478ff[rapidViewId=11,state=CLOSED,name=ARCADE Sprint 114,startDate=2016-10-20T14:25:40.557+01:00,endDate=2016-11-03T14:25:00.000Z,completeDate=2016-11-04T14:16:23.604Z,sequence=3748,id=3748]\")"
  expectedDF <- data.frame(team=c("ARCADE","ARCADE" ), sprint=c(113,114) )

  testHelperExtractTeamAndSprint( issueSprints , expectedDF , functionNameSelf )  
} 


SprintTextMustBeCaseInsensitive <- function ( callstack=sys.calls() ) {
  functionNameSelf <- callstack[[6]]

  issueSprintsCaps <- "c(\"com.atlassian.greenhopper.service.sprint.Sprint@50eaa052[rapidViewId=11,state=CLOSED,name=ARCADE Sprint 113,startDate=2016-10-06T14:40:52.687+01:00,endDate=2016-10-20T14:40:00.000+01:00,completeDate=2016-10-21T06:32:06.424+01:00,sequence=3713,id=3713]\")"
  issueSprintsSmall <- "c(\"com.atlassian.greenhopper.service.sprint.Sprint@50eaa052[rapidViewId=11,state=CLOSED,name=ARCADE sprint 113,startDate=2016-10-06T14:40:52.687+01:00,endDate=2016-10-20T14:40:00.000+01:00,completeDate=2016-10-21T06:32:06.424+01:00,sequence=3713,id=3713]\")"
  
  actualDFwithCaps <- getTeamAndSprint(issueSprintsCaps)
  actualDFwithSmall <- getTeamAndSprint(issueSprintsSmall)

  actualDFwithCaps <- data.frame(lapply(actualDFwithCaps,as.character),stringsAsFactors = F)
  actualDFwithSmall <- data.frame(lapply(actualDFwithSmall,as.character),stringsAsFactors = F)
  
  if ( identical(actualDFwithCaps,actualDFwithSmall) ) { 
    print ( paste( functionNameSelf , ": OK"))
  } else {
    print ( paste( functionNameSelf , ": FAIL"))
  }
  
} 

MultiWordTeamNamesMustBeSupported  <- function ( callstack=sys.calls() ) {
  functionNameSelf <- callstack[[6]]
  
  issueSprints <- "c(\"com.atlassian.greenhopper.service.sprint.Sprint@50eaa052[rapidViewId=11,state=CLOSED,name=ARC Pisa Sprint 119,startDate=2016-10-06T14:40:52.687+01:00,endDate=2016-10-20T14:40:00.000+01:00,completeDate=2016-10-21T06:32:06.424+01:00,sequence=3713,id=3713]\")"
  expectedDF <- data.frame(team=c("ARC Pisa"), sprint=c(119) )
  
  testHelperExtractTeamAndSprint( issueSprints , expectedDF , functionNameSelf )  
}  



MultipleSpacesInTeamNamesToBeNormalized  <- function ( callstack=sys.calls() ) {
  functionNameSelf <- callstack[[6]]
  
  issueSprints <- "c(\"com.atlassian.greenhopper.service.sprint.Sprint@50eaa052[rapidViewId=11,state=CLOSED,name=ARC   Pisa Sprint 119,startDate=2016-10-06T14:40:52.687+01:00,endDate=2016-10-20T14:40:00.000+01:00,completeDate=2016-10-21T06:32:06.424+01:00,sequence=3713,id=3713]\")"
  expectedDF <- data.frame(team=c("ARC Pisa"), sprint=c(119) )
  
  testHelperExtractTeamAndSprint( issueSprints , expectedDF , functionNameSelf )  
}  

AcceptanceTestSuite <- function () {
  MultipleSprintsCanBeExtracted()
  SprintTextMustBeCaseInsensitive()
  MultiWordTeamNamesMustBeSupported()
  MultipleSpacesInTeamNamesToBeNormalized()
}


## Test Execution Starts Here  
AcceptanceTestSuite()


