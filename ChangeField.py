# Change Jira number custom filed value
# 1) using REST API
# 2) using Python lib

# 27.7.2019 mika.nokka1@gmail.com 
# 
# NOTES:
# 1) For this POC removed .netrc authetication, using pure arguments
# 2) Requires Jira issue as a parameter (issue holds numberic custom field to be changed)
#
# Using Python V2
#
#from __future__ import unicode_literals

#import openpyxl 
import sys, logging
import argparse
#import re
from collections import defaultdict
from Authorization import Authenticate  # no need to use as external command
from Authorization import DoJIRAStuff

import glob
import re
import os
import time
import unidecode
from jira import JIRA, JIRAError
from collections import defaultdict
from time import sleep
import keyboard
import math
import requests
import json
import random 
import time

#from pandas._libs.interval import numbers

start = time.clock()
__version__ = u"0.1"

# should pass via  parameters
#ENV="demo"
ENV=u"PROD"

logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    logging.debug (u"--Starting operations --") 

 
    parser = argparse.ArgumentParser(description=" Set value of Jira custom field / Insigth object attribute / simulate custom fields / Insight attribute values constant changes",
    
    
    epilog="""
    
    EXAMPLES:
    
    1) Change numeric customfield (defined in args)
    ChangeField.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -c CUSTOMFIELDID -v NUMBERVALUEFORCUSTOMFIELD -i JIRAISSUE
    2) Feed constant feed of data for (hardcoded) customfields
    ChangeField.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -c CUSTOMFIELDID -v NUMBERVALUEFORCUSTOMFIELD -i JIRAISSUE -o simu
    3) Feed constant feed of data for (harcoded) Mindville Insight object attributes
    ChangeField.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -c CUSTOMFIELDID -v NUMBERVALUEFORCUSTOMFIELD -i JIRAISSUE -o simuninsght
     """

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-i', help='<JIRA issue',metavar="jira_issue")
    parser.add_argument('-c', help='<Customfield ID>',metavar="customfieldname")
    parser.add_argument('-l', help='<Value for customfield>',metavar="customfield_value")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. Off by default>',metavar="on|off",default="off")
    parser.add_argument('-o', help='<Execute small hardcoded  livefeed simulator changing hardcode custom field values (on) / Insigth object attribute values (simuinsight). Off by default>',metavar="on|off|simuinsight",default="off")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    CFIELD=args.c or ''
    CVALUE=args.l or ''
    ISSUE=args.i or ''
    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    
    #logging.info("SKIP:{0}".format(SKIP))
    if (args.o=="on"):
        SIMUL="on"
    elif (args.o=="insight"):   
        SIMUL="insight"
    elif (args.o=="simuinsight"):   
        SIMUL="simuinsight"    
    else:
        SIMUL="off"
    
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' or CFIELD=='' or CVALUE=='' or ISSUE==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    # used when pytyhon jira lib used, just overhead in this case 
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    # Change value as stated in tool parameters
    if (SIMUL=="off"):
        Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE,ISSUE)
    elif (SIMUL=="on"):
        # Fakes live feed for three numberic Jira custom fields, mimicing counters
        SIMU(ISSUE,jira)
    
    elif (SIMUL=="insight"):
        # set soem hardcode Insight Object attribures
        Insight(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE,ISSUE)
        
    elif (SIMUL=="simuinsight"):
        # set soem hardcode Insight Object attribures
        INSIGHTSIMU(PSWD,USER)   
        
    else:
        logging.error("\n Dont know what to do!!\n ")
         



############################################################################################################################################
# Do the Jira operations
#

def Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE,ISSUE):

     
    #TODO: remove read only field protection      
    
    #WORKS, using REST API, setting number custom field value
    #try:
    #payload = {"fields": {"customfield_10128": "37777756"}} 
    #  payload = {"fields": {"customfield_10127": 666634543}} 
    #  url = 'https://jirapoc.ambientia.fi/rest/api/2/issue/LIV-1/'

    #  headers = {
    #  'Content-Type': 'application/json',
    #  'Accept': 'application/json',
    #  }
    #r=requests.put(url, headers=headers, json=payload,auth=(USER, PSWD))   
    #r=requests.post(url, headers=headers, data=json.dumps(payload),auth=(USER, PSWD))    
    #  r=requests.put(url, headers=headers, json=payload,auth=(USER, PSWD))   
    #  print(r)     
    #  print (r.text   )   
    #not correct trappinng
    #except JIRAError as e: 
    #                    logging.debug(" ********** JIRA ERROR DETECTED: ***********")
    #                    logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                        #sys.exit(5) 
    #else: 
    #    logging.debug("All OK") 
     
       
    # Setting using Python Jira lib (REST API wrapper)
    issue = jira.issue(ISSUE)
    
    try:
               
            fieldtag="customfield_"+CFIELD 
            mydict = {'{0}'.format(fieldtag):  int(CVALUE)} 
            issue.update(fields=mydict) 
                  
    except JIRAError as e: 
                        logging.debug(" ********** JIRA ERROR DETECTED: ***********")
                        logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                        #sys.exit(5) 
    else: 
        logging.debug("Issue update OK") 
    # TODO: return readonly field protection
    
           
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")    
    #logging.debug ("--Script exiting. Bye!--")




############################################################################################################################################
# Use hardcoded three numberic customfield IDs to mimic consta data feed to these fields
#

def SIMU(ISSUE,jira):

    COUNTER=10
    issue = jira.issue(ISSUE)
    while (COUNTER>0): 
       Updater(issue,10127,(random.randint(1, 1000)),jira) 
       Updater(issue,10129,(random.randint(1, 1000)),jira)
       Updater(issue,10130,(random.randint(1, 1000)),jira)
       COUNTER=COUNTER-1
        
       logging.debug("Sleeping 5 secs")
       time.sleep(5)
       
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))   
    return 
  
#####################################################################################################
# Use hardcode Mindville Insight object info to feed constant data to these object attribute fields
#


def INSIGHTSIMU(PSWD,USER):

    COUNTER=10
    VALUE=4567
    VALUE2=1
    VALUE3=100
    VALUE4=50
    while (COUNTER>0): 

      InsightUpdater(PSWD,USER,"SHERVOL2-54",7,39,VALUE)
      InsightUpdater(PSWD,USER,"SHERVOL2-54",7,40,VALUE2)
      InsightUpdater(PSWD,USER,"SHERVOL2-55",7,39,VALUE3)
      InsightUpdater(PSWD,USER,"SHERVOL2-55",7,40,VALUE4)
      COUNTER=COUNTER-1
      VALUE=VALUE+100
      VALUE2=VALUE2+900
      VALUE3=VALUE3+37
      VALUE4=VALUE4+111
      
      logging.debug("Sleeping 5 secs")
      time.sleep(5)
       
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))   
    return 
  
  
 
##########################################################################
# Update Jira numeric customfield
#
def Updater(ISSUE,CFIELD,CVALUE,jira):    


    try:           
            issue = jira.issue(ISSUE)
            fieldtag="customfield_"+str(CFIELD) 
            mydict = {'{0}'.format(fieldtag):  int(CVALUE)} 
            issue.update(fields=mydict) 
                  
    except JIRAError as e: 
                        logging.debug(" ********** JIRA ERROR DETECTED: ***********")
                        logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                        #sys.exit(5) 
    else: 
        logging.debug("Issue {0} (customfield_{1} value:{2} )updated OK".format(issue,CFIELD,CVALUE)) 
    # TODO: return readonly field protection
    
#################################################################################
# Test function how Insight attribute is changed
#
def Insight(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE,ISSUE):
    
    print ("Insight operation")


    VALUE=15566655
    OBJECTISSUEID="SHERVOL2-54"
    OBJECTID=7
    ATTRIBUTEID=39
    InsightUpdater(PSWD,USER,OBJECTISSUEID,OBJECTID,ATTRIBUTEID,VALUE)
    print ("bye")
    exit(5)

    try:
  
    # REST API DOC: https://insight-javadoc.riada.io/insight-javadoc-8.6/insight-rest/#object__id__put 
      payload3 = {
  "objectTypeId": 7,
  "attributes": [
    {
      "objectTypeAttributeId": 39,
      "objectAttributeValues": [
        {
          "value": "555555"
        },
      ]
    }
  ]
}
        
      url='https://jirapoc.ambientia.fi/rest/insight/1.0/object/SHERVOL2-54'

      headers = {
    'Content-Type': 'application/json',
     'Accept': 'application/json',
     }
    
      r=requests.put(url, headers=headers, json=payload3,auth=(USER, PSWD))   
      print(r)     
      print (r.text   )   
    
      
    except requests.exceptions.HTTPError as errh:
       logging.debug ("Http Error: {0}".format(errh))
    except requests.exceptions.ConnectionError as errc:
       logging.debug ("Error Connecting: {0}".format(errc))
    except requests.exceptions.Timeout as errt:
       logging.debug ("Timeout Error: {0}".format(errt))
    except requests.exceptions.RequestException as err:
       logging.debug ("Geeneral Error? {0}".format(err))

    else: 
        logging.debug("All OK") 


###############################################################################
# Update Mindville Insight object attributes
#
#
def InsightUpdater(PSWD,USER,OBJECTISSUEID,OBJECTID,ATTRIBUTEID,VALUE):
      
    print ("Insight updater working")
    try:
    # REST API DOC: https://insight-javadoc.riada.io/insight-javadoc-8.6/insight-rest/#object__id__put 
      payload3 = {
  "objectTypeId": "{0}".format(OBJECTID),
  "attributes": [
    {
      "objectTypeAttributeId": "{0}".format(ATTRIBUTEID),
      "objectAttributeValues": [
        {
          "value": "{0}".format(VALUE)
        },
      ]
    }
  ]
}
        
      url='https://jirapoc.ambientia.fi/rest/insight/1.0/object/{0}'.format(OBJECTISSUEID)

      headers = {
    'Content-Type': 'application/json',
     'Accept': 'application/json',
     }
    
      r=requests.put(url, headers=headers, json=payload3,auth=(USER, PSWD))   
      #print(r)     
      #print (r.text   )   
      
    except requests.exceptions.HTTPError as errh:
       logging.debug ("Http Error: {0}".format(errh))
    except requests.exceptions.ConnectionError as errc:
       logging.debug ("Error Connecting: {0}".format(errc))
    except requests.exceptions.Timeout as errt:
       logging.debug ("Timeout Error: {0}".format(errt))
    except requests.exceptions.RequestException as err:
       logging.debug ("Geeneral Error? {0}".format(err))

    else: 
        logging.debug("All OK") 


if __name__ == "__main__":
    main(sys.argv[1:]) 