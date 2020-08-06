@echo off
md ..\output
md ..\reports

call python consolidate_raw_data.py > ..\output\consolidated.csv
call python prepare_data_for_management_reports.py ..\output\consolidated.csv ..\output\actualdata.csv
call python generate_management_reports_from_template.py ..\output\actualdata.csv  ..\templates\management_report_template.xlsx ..\reports
