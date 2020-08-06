import sys
from TimeSheetWorkbook import TimeSheetWorkbook
from CoordinatorWorkbook import CoordinatorWorkbook

import glob
import os


def GetTeamName(filename):
    teamname = filename.replace('.xlsm', '')
    arr = teamname.split()
    teamname = arr[len(arr)-1]
    return teamname
    
def PrintTeamEffortData():
    files = glob.glob("../teams/Effort*.xlsm", recursive=False)
    for workbookName in files:
        teamName = GetTeamName(workbookName)
        wb = TimeSheetWorkbook(workbookName)
        data = wb.GetMeltedData()
        for row in data:
            listToStr = ','.join([str(elem) for elem in row.values()])
            print(teamName + "," + listToStr)


def PrintCoordinatorData():
    workbookName = "../teams/coordinators.xlsx"
    wb = CoordinatorWorkbook(workbookName)
    data = wb.GetMeltedData()
    for row in data:
        listToStr = ','.join([str(elem) for elem in row.values()])
        print(listToStr)

print("Team,WorkStream,Iteration,Member,Date,Activity,Effort")
PrintTeamEffortData()
PrintCoordinatorData()


