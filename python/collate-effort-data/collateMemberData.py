import sys
from TimeSheetWorkbook import TimeSheetWorkbook

workbookName = sys.argv[1]
wb = TimeSheetWorkbook(workbookName)
data = wb.GetMeltedData()

#'WorkStream': 'WS1',
#'Iteration': 1,
#'Member': 'aashish',
#'Day': '14-Jul',
#'Effort': 6

for row in data:
    listToStr = ','.join([str(elem) for elem in row.values()])
    print(listToStr)
