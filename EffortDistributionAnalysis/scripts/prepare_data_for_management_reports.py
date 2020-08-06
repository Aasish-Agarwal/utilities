import pandas as pd
import numpy as np
import sys
from EffortsDataProcessor import EffortsDataProcessor
start_date = '08-01-2020'
end_date = '08-31-2020'

consolidated_data_file = sys.argv[1]
data_for_reports_file = sys.argv[2]

consolidated_csv = EffortsDataProcessor(consolidated_data_file , start_date,end_date)
df = consolidated_csv.GetData()
df.to_csv(path_or_buf = data_for_reports_file , index=False)


#consolidated_csv = EffortsDataProcessor("./output/consolidated.csv" , start_date,end_date)
#df = consolidated_csv.GetData()
#df.to_csv(path_or_buf = "./output/actualdata.csv", index=False)
