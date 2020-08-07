import pandas as pd
import numpy as np
import sys
import shutil
from openpyxl import load_workbook

from EffortsDataProcessor import EffortsDataProcessor
start_date = '08-01-2020'
end_date = '08-31-2020'

skip_team = sys.argv[1]
report_template_file = sys.argv[2]
consolidated_data_file = sys.argv[3]
data_for_validation_file = sys.argv[4]


def GenerateReport( df , outfile ):   
    shutil.copyfile(report_template_file, outfile )

    book = load_workbook(outfile)
    writer = pd.ExcelWriter(outfile, engine='openpyxl') 
    writer.book = book

    ## ExcelWriter for some reason uses writer.sheets to access the sheet.
    ## If you leave it empty it will not know that sheet Main is already there
    ## and will create a new sheet.
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, "completeness", index = False)
    writer.save()


consolidated_csv = EffortsDataProcessor(consolidated_data_file , start_date,end_date)
df = consolidated_csv.GetData()

validation_df = df[['Team','WorkStream','Member','Date']]


validation_df = validation_df.drop_duplicates()

mask = (validation_df['Team'] != skip_team)
validation_df = validation_df.loc[mask]
GenerateReport(validation_df , data_for_validation_file)

#validation_df.to_csv(path_or_buf = data_for_validation_file , index=False)

