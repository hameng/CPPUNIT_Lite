import fileinput
import sys
import glob
import os


test_name="APIs_Test" ##sys.argv[1]
 
##path_dir = sys.argv[1]
path_dir="c:/123/123.log"
 
 
path=os.path.join(path_dir)

#print path
logfile=None

testCaseStats = {'tests': 0, 'failures':0, 'errors':0, 'skipped':0}
testCaseName = ""
testCasesList = {}
testResult= {}
testList=[]
suiteList=[]
failure=False
 
 
 
 
 
################# GET RIGHT LOG FILE ##########################
def getLogfile(path):
    global logfile
    global failure
    res=os.path.exists(path)
    if res==True:
        logfile=path
        failure=False
    else:
        failure=True
        
############# CREATE DICTIONAR #####################
def createDic(logfile): 
  
    prev_testSuiteName=''
    open_file=open(logfile, 'r')
    ##lines = open_file.readlines()

    for line in open_file:   
    ##for line in fileinput.input(logfile):  
        ###############get test suites #################
 
        if "[TEST-RUN]" in line:
            ##print line 
            temp_testSuiteName= line.strip().split("<SUITE>")[1].split("<TEST>")[0].strip()
            testcaseName=line.strip().split("<SUITE>")[1].split("<TEST>")[1].strip().split()[0]
            
            ##testSuiteName =line.strip().strip(',').replace(' ','')
            if temp_testSuiteName!=prev_testSuiteName:
                testSuiteName=temp_testSuiteName
                prev_testSuiteName=testSuiteName
                testCaseStats[testSuiteName] = {'tests': 0, 'failures': 0, 'errors':0, 'skipped':0}
                #print testSuiteName
                #testResult[testSuiteName]={'list':[]}
                testResult[testSuiteName]=[]
                suiteList.append(testSuiteName)
                #print testSuiteName
                ##newTest = False
            ##print testcaseName    
            testResult[testSuiteName].append(testcaseName)
            ##testResult[testSuiteName]['list'].append(testcaseName)
            ##print testSuiteName + "+" + testcaseName
            unittest=testSuiteName + "+" + testcaseName
            #print unittest
            testList.append(unittest)
            
            #print testResult[testSuiteName]
            ##full_testcaseName=testSuiteName + ":" + testcaseName
            ##print full_testcaseName
            testCaseStats[testSuiteName][testcaseName]= {'passed':-1, 'errormsg':[]}
            
            
        elif ("***** TESTCASE PASS" in line):
            testCaseStats[testSuiteName]['tests'] =  testCaseStats[testSuiteName]['tests']+1
            testCaseStats['tests'] = testCaseStats["tests"]+1
            
            testCaseStats[testSuiteName][testcaseName]['passed'] = 1
        
        elif ("***** TESTCASE FAIL" in line):
            testCaseStats[testSuiteName]['failures'] =  testCaseStats[testSuiteName]['failures']+1
            testCaseStats['failures'] = testCaseStats["failures"]+1
            
            testCaseStats[testSuiteName]['tests'] =  testCaseStats[testSuiteName]['tests']+1
            testCaseStats['tests'] = testCaseStats["tests"]+1
            
            testCaseStats[testSuiteName][testcaseName]['passed'] = 0
            
        elif ("Failure_Msg: " in line):
            errormsg= line.replace("&","and") 
            errormsg= errormsg.replace("&&","and")+". "
            #testCaseStats[testSuiteName][testcaseName]['errormsg']=testCaseStats[testSuiteName][testcaseName]['errormsg']+errormsg
            testCaseStats[testSuiteName][testcaseName]['errormsg'].append(errormsg)
        
####################### CREATE XML REPORT #########################################
def createXML():
        
    ##print testResult
    ##print testList
    #for testSuiteName, tests in testResult.items(): 
  
    for suite in suiteList:
        testSuiteName = suite
        for unitest in testList:
            suiteName = unitest.split("+")[0] 
            test = unitest.split("+")[1] 
            if  suiteName == testSuiteName:
                if(testCaseStats[testSuiteName][test]['passed']==-1):
                    testCaseStats['tests'] = testCaseStats["tests"]+1
                    testCaseStats['errors']=testCaseStats['errors']+1
                   
                    testCaseStats[testSuiteName]['tests'] =  testCaseStats[testSuiteName]['tests']+1
                    testCaseStats[testSuiteName]['errors']=testCaseStats[testSuiteName]['errors']+1
     
     
    result_xml = open(test_name+"_Junit"+".xml", "w")
    result_xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    result_xml.write("<testsuite name=\" %s\" tests=\"%s\"\
     failures=\"%s\" errors=\"%s\" skipped=\"%s\" >\n"\
    %(test_name, testCaseStats['tests'], testCaseStats['failures'], testCaseStats['errors'], testCaseStats['skipped']))   
    
                
    for suite in suiteList:
        testSuiteName = suite
        result_xml.write("\t<testsuite name=\"%s\" tests=\"%s\" failures=\"%s\" errors=\"%s\" skipped=\"%s\" >\n" \
                         %(testSuiteName, testCaseStats[testSuiteName]['tests'], testCaseStats[testSuiteName]['failures'], testCaseStats[testSuiteName]['errors'], testCaseStats[testSuiteName]['skipped'])) 
        ##testSuiteName = unitest.split("+")[0] 
        ##test = unitest.split("+")[1]  
        for unitest in testList:
            suiteName = unitest.split("+")[0] 
            test = unitest.split("+")[1] 
            if  suiteName == testSuiteName:
                result_xml.write("\t\t<testcase classname=\"%s__%s\"\
                name=\"%s\" time=\"0.1\">\n" %(testSuiteName,test , test))
                    
                if(testCaseStats[testSuiteName][test]['passed']==0):
                    errmsg =testCaseStats[testSuiteName][test]['errormsg']
                    result_xml.write("\t\t\t<failure message=\"Failed\" type=\"Failed\"> ")
                    for err in errmsg:
                        #result_xml.write("\t\t\t<failure message=\"Failed\" type=\"Failed\">%s</failure>\n"%( err ))
                        result_xml.write("%s\n"%(err))
                    result_xml.write("</failure>\n")   
                elif(testCaseStats[testSuiteName][test]['passed']==-1):
                    result_xml.write("\t\t\t<failure message=\"Failed\" type=\"Failed\"><a> Test Crashed </a></failure>\n" ) 
                result_xml.write("\t\t</testcase>\n")
        result_xml.write("\t</testsuite>\n")
    result_xml.write("\t</testsuite>\n")
    result_xml.close();
    print test_name+"Junit.xml  created"

 
######CREATE TEST.txt  - <pass> <failed> <not_run> <total> ######
def createTXT():
    result_txt = open(test_name+"_"+".txt","w")
    int_failed = testCaseStats['failures']
    int_notrun = testCaseStats['errors']+testCaseStats['skipped']
    int_total = testCaseStats['tests']
    int_pass = int_total - int_notrun - int_failed
    
    print "Passed:%s. Failed:%s. Not_Run:%s. Total:%s. "%(int_pass,int_failed,int_notrun,int_total)
    
    result_txt.write("TestSuite: %s\n"%(test_name))
    result_txt.write("TestStatus:Succeed\n")
    result_txt.write("PASSED:%s\n"%(int_pass))
    result_txt.write("FAILED:%s\n"%(int_failed))
    result_txt.write("NOT_RUN:%s\n"%(int_notrun))
    result_txt.write("TOTAL:%s\n"%(int_total))
    result_txt.close();
    print test_name+".txt created"
    
    
def main():
    getLogfile(path)
    #### LOG FILE EXISTED####
    if (not failure):
        createDic(logfile)
        createXML()
        createTXT()
    else:
        print "No such log file"
        result_txt = open(test_name+".txt","w")
        result_txt.write("TestSuite: %s\n"%(test_name))
        result_txt.write("TestStatus:Failure\n")
        result_txt.close();
    
if __name__ == '__main__':
    main()   

