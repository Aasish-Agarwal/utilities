echo WorkStream,Iteration,Member,Day,Category,Activity,Effort > consolidated.csv
python collateMemberData.py WorkStream1.xlsm >> consolidated.csv
python collateMemberData.py WorkStream2.xlsm >> consolidated.csv
python collateMemberData.py WorkStream3.xlsm >> consolidated.csv
