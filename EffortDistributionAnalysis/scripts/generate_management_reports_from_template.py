import pandas as pd
import numpy as np
import sys
import shutil
from openpyxl import load_workbook

data_for_reports_file = sys.argv[1]
report_template_file = sys.argv[2]
output_folder = sys.argv[3]
master_df = pd.read_csv(data_for_reports_file, sep=',')

def GenerateReport( df , outfile ):   
    shutil.copyfile(report_template_file, outfile )

    book = load_workbook(outfile)
    writer = pd.ExcelWriter(outfile, engine='openpyxl') 
    writer.book = book

    ## ExcelWriter for some reason uses writer.sheets to access the sheet.
    ## If you leave it empty it will not know that sheet Main is already there
    ## and will create a new sheet.
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, "actualdata", index = False)
    writer.save()

def GenerateReportForWorkStreams():
    df = master_df
    for ws in df['WorkStream'].unique():
        mask = (df['WorkStream'] == ws)
        ws_df = df.loc[mask]
        ws_report_file = output_folder+"/Efforts Distribution Report - "+ws+".xlsx"
        GenerateReport( ws_df , ws_report_file )
    
def GenerateOrgViewReport():
    df = master_df
    management_report_file = output_folder+"/"+"ManagamentReport.xlsx"
    GenerateReport(df,management_report_file)

GenerateOrgViewReport()
GenerateReportForWorkStreams()
