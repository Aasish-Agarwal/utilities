#Jenkins Build Report Analysis
Use this tool to find how much does it take for you to recover from the failed builds

#Steps to use

## Download build deails xml file
https://<jenkins installation>/job/<jobname>/rssAll

## save xml to disk

## use following command to get the statistics
python analyzebuilds.py [build history xml file]

#Expected output

you must see something similar to this on your screen

Failed In,Recovered In,Failed Time,Recovered Time,Delay in Munutes
1623,1629,2019-08-07T14:00:00Z,2019-08-08T13:56:01Z,1436
1615,1621,2019-08-07T06:00:00Z,2019-08-07T11:46:40Z,346
1612,1613,2019-08-06T12:00:00Z,2019-08-06T12:58:01Z,58
1600,1603,2019-08-02T14:00:00Z,2019-08-05T05:33:15Z,3813

#Prerequisite
Python 3.7+
