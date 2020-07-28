# Chagne Jira custom filed value
# 1) using REST API
# 2) using Python lib

# 27.7.2019 mika.nokka1@gmail.com 
# 
# NOTES:
# 1) For this POC removed .netrc authetication, using pure arguments
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

 
    parser = argparse.ArgumentParser(description=" Set value of Jira custom field",
    
    
    epilog="""
    
    EXAMPLE:
    
    ChangeField.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -c CUSTOMFIELDNAME -v \"Value for custom field\" """

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-c', help='<Customfield ID>',metavar="customfieldname")
    parser.add_argument('-l', help='<Value for customfield>',metavar="customfield_value")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. Off by default>',metavar="on|off",default="off")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    CFIELD=args.c or ''
    CVALUE=args.l or ''
    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    
    #logging.info("SKIP:{0}".format(SKIP))
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' or CFIELD=='' or CVALUE==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    # used when pytyhon jira lib used, just overhead in this case 
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE)



############################################################################################################################################
# Parse attachment files and add to matching Jira issue
#

#NOTE: Uses hardcoded sheet/column value

def Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,CFIELD,CVALUE):

    # Change these according the need, or add as program arguments
 
 
    logging.info("SKIP:{0}".format(SKIP))
    logging.info("CVALUE:{0}".format(CVALUE))
    logging.info("CFIELD:{0}".format(CFIELD))  
           
    #"customfield_10010": 42.07       
    
    #test, get all project info
    #response = requests.get('https://jirapoc.ambientia.fi/rest/api/2/project', auth=(USER, PSWD))
    #print(response)     
    #print (response.json()) 
           
           
    
    
    #payload = {"customfield_10127": 707}
    #r = requests.put('https://jirapoc.ambientia.fi/rest/api/2/issue/LIV-1', params=payload,auth=(USER, PSWD))
    #print(r)     
    #print (r.json()   )                     
     
     
    #TODO: remove read only field protection      
    #payload = {"fields": {"customfield_10127": "456"}} 
    #payload = {"fields": {"customfield_10128": "5555456"}} 

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
    issue = jira.issue('LIV-1')
    
    try:
            #fieldtag="customfield_"+CFIELD #+"= 44445"
            #myvalue=78787
            #fieldtag2=json.load(fieldtag)
            #print ("fieldtag:{0}".format(fieldtag))
            #issue.update("\'{0}\'".format(fieldtag)) 
            #issue.update(fields={"fields={\'{0}\'".format(fieldtag): myvalue "}" })    
            # works: issue.update(fields={'customfield_10127': 77777})  
           
           #WORKS 
           # mydict = {
           #     'customfield_10127':  123}
                
           # issue.update(fields=mydict)
            
            
            fieldtag="customfield_"+CFIELD 
            myvalue=12345
            mydict = {'{0}'.format(fieldtag):  int(myvalue)} 
            issue.update(fields=mydict) 
            
            
            
            
            
            #issue.update("fields={0}: {1}".format(fieldtag,myvalue))
    except JIRAError as e: 
                        logging.debug(" ********** JIRA ERROR DETECTED: ***********")
                        logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                        #sys.exit(5) 
    else: 
        logging.debug("issue update on") 
    # TODO: return readonly field protection
    
           
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
    
logging.debug ("--Script exiting. Bye!--")



#############################################
# Generate timestamp 
#
def GetStamp():
    from datetime import datetime,date
    
    hours=str(datetime.today().hour)
    minutes=str(datetime.today().minute)
    seconds=str(datetime.today().second)
    milliseconds=str(datetime.today().microsecond)

    stamp=hours+"_"+minutes+"_"+seconds+"_"+milliseconds

    return stamp


if __name__ == "__main__":
    main(sys.argv[1:]) 