import re
import xml.etree.ElementTree as ET
import datetime
import sys

class BuildDetails:
        def setStatus(self, title):
                self.title = title
        def setNumber(self, number):
                self.number = number
        def setTime(self, time):
                self.time = time
        def getStatus(self):
                return self.title
        def getTime(self):
                return self.time
        def getNumber(self):
                return self.number

class JenkinsBuildSummaryAnalyzer:
        def __init__(self):
                pass

        def printRawData(self):
                for x in self.buildlist:
                        print(x.getNumber(), x.getTime(), x.getStatus() , sep = ',')
        def GetRawBuildData(self, build ):
                bd = BuildDetails()
                for details in build:
                        if ( details.tag == '{http://www.w3.org/2005/Atom}title'):
                                line = details.text
                                titlePattern = re.compile(".*#([\d]*)\s+\((.*)\)")
                                m = titlePattern.match(line)
                                bd.setNumber(m.groups()[0])
                                bd.setStatus(m.groups()[1])
                                #print('title', details.text)
                        if ( details.tag == '{http://www.w3.org/2005/Atom}published'):
                                bd.setTime(details.text)
                                #print('published', details.text)
                return (bd)
                
        def CollectRawData(self):
                self.buildlist = []
                for child in self.root:
                        if ( child.tag == '{http://www.w3.org/2005/Atom}entry'):
                                bd = self.GetRawBuildData(child)
                                self.buildlist.append(bd)
                
        def analyzeBuilds(self):
                self.summaryStat = []
                rectime = ''
                recbuild = ''
                for build in self.buildlist:
                        if ( build.getStatus() == 'back to normal'):
                                rectime = build.getTime()
                                recbuild = build.getNumber()
                        if ( build.getStatus() == 'broken since this build'):
                                if len(rectime) > 0:
                                        summary = {}
                                        fmtstr = '%Y-%m-%dT%H:%M:%SZ'
                                        startdate = datetime.datetime.strptime(build.getTime(), fmtstr)
                                        enddate = datetime.datetime.strptime(rectime, fmtstr)
                                        delta = enddate - startdate
                                        summary['from'] = build.getNumber()
                                        summary['to'] = recbuild
                                        summary['fromtime'] = build.getTime()
                                        summary['totime'] = rectime
                                        summary['delay'] = (delta.days * 24 * 60) + int(delta.seconds/60)
                                        rectime = ''
                                        self.summaryStat.append(summary)

        def AnalyzeFromXML(self , xmlfile ):
                tree = ET.parse(xmlfile)
                self.root = tree.getroot()
                self.CollectRawData()
                self.analyzeBuilds()
        def GetBuildSummary(self):
                return (self.summaryStat)
