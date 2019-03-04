/**
 * @OnlyCurrentDoc Limits the script to only accessing the current sheet.
 */

/**
 * A special function that runs when the spreadsheet is open, used to add a
 * custom menu to the spreadsheet.
 */
function onOpen() {
  var spreadsheet = SpreadsheetApp.getActive();
  var menuItems = [
    {name: 'Update', functionName: 'evaluateQuiz_'}
  ];
  spreadsheet.addMenu('QuizResults', menuItems);
}


/**
 * Read the responses, compare them with reference, and update results.
 *
 */
function evaluateQuiz_() {
  resetResultsSheet_();
  var responseRowValues = getResponses_();
  
  for (var response = 0; response < responseRowValues.length ; response++) {
    var memberName = responseRowValues[response][0];
    var memberEmail = responseRowValues[response][1];
    var correctAnswers = getCorrectAnswers_(responseRowValues[response]);
    appendResults_(memberName , memberEmail ,  correctAnswers );
  }
}


/**
 * Read the responses, return the dataset.
 *
 */
function getResponses_() {
  var spreadsheet = SpreadsheetApp.getActive();
  var responseSheet = spreadsheet.getSheetByName('response');
  
  const numResponses = responseSheet.getLastRow()  - 1;
  const numQuestions = getQuestionCount_() ;
  const startingColumn = 2;
  const startingRow = 2;
  
  const identityFieldCount = 2;
  
  var responseRow = responseSheet.getRange(startingRow, startingColumn, numResponses, numQuestions + identityFieldCount);
  var responseRowValues = responseRow.getValues();
  
  return responseRowValues;
}


/**
 * Compare each result row, with teh reference results.
 *
 */

function getCorrectAnswers_( response ) {
  var correctAnswers = 0;
  var referenceDataValues = getReferenceResults_();
  const identityFieldCount = 2;

  for (var question = 0; question < referenceDataValues.length ; question++) {
    if (  response[question+2] == referenceDataValues[question][0]) {
      correctAnswers++;
    } 
  }

  return correctAnswers;
}




/**
 * A custom function to reset result sheet.
 *
 */
function resetResultsSheet_() {
  var spreadsheet = SpreadsheetApp.getActive();
  var resultSheet = spreadsheet.getSheetByName('results');
  
  resultSheet.deleteRows(1, resultSheet.getLastRow());
  resultSheet.appendRow(['Name'	,'eMail'	, 'Correct Answers'	,'Total Questions'	,'Correct Percentage']);
}

/**
 * A custom function to append results.
 *
 */
function appendResults_( name, email, correctAnswers ) {
  var spreadsheet = SpreadsheetApp.getActive();
  var resultSheet = spreadsheet.getSheetByName('results');

  var questionCount =getQuestionCount_( );
  
  var correctPct = (correctAnswers * 100.0 ) / questionCount;
  
  resultSheet.appendRow([name, email, correctAnswers, questionCount, correctPct]);
}


/**
 * A custom function to get question count.
 *
 */
function getQuestionCount_( ) {
  var spreadsheet = SpreadsheetApp.getActive();
  var referenceSheet = spreadsheet.getSheetByName('ref');
  
  const numQuestions = referenceSheet.getLastRow() ;
  return numQuestions;
}


function getReferenceResults_() {
  var spreadsheet = SpreadsheetApp.getActive();
  const numQuestions = getQuestionCount_();

  var referenceSheet = spreadsheet.getSheetByName('ref');
  var referenceDataRow = referenceSheet.getRange(1, 2, numQuestions, 1);
  var referenceDataValues = referenceDataRow.getValues();

  return referenceDataValues;
}

