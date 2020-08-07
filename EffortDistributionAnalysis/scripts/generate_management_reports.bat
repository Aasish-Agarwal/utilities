@echo off
md ..\output
md ..\reports

set CONSOLIDATED=..\output\consolidated.csv
set DATA_FOR_REPORT=..\output\actualdata.csv
set MGMT_TEMPLATE=..\templates\management_report_template.xlsx
set VALIDATION_TEMPLATE=..\templates\completion_validation_template.xlsx
set STATUS_REPORT=..\reports\status.xlsx
set REPORTS_FOLDER=..\reports

call python consolidate_raw_data.py > %CONSOLIDATED%
call python prepare_data_for_management_reports.py %CONSOLIDATED% %DATA_FOR_REPORT%
call python generate_management_reports_from_template.py %DATA_FOR_REPORT%  %MGMT_TEMPLATE% %REPORTS_FOLDER%
call python prepare_data_for_completeness_validation.py Coordinators %VALIDATION_TEMPLATE% %CONSOLIDATED% %STATUS_REPORT%
