import sys

from JenkinsBuildSummaryAnalyzer import JenkinsBuildSummaryAnalyzer

def main():
        if ( len(sys.argv) > 1 ) :
                ba = JenkinsBuildSummaryAnalyzer()
                ba.AnalyzeFromXML(sys.argv[1])
                print('Failed In' , 'Recovered In' , 'Failed Time',  'Recovered Time' , 'Delay in Munutes',sep = ',')
                for summary in ba.GetBuildSummary():
                        print( summary['from'] , summary['to'] , summary['fromtime'] , summary['totime'] , summary['delay'], sep = ',')
        else:        
                print('usage: python' , sys.argv[0], '[build history xml file]')
main()

