# JiraRestApiCustomfielder
POC example, use REST API to change Jira numberic customfield value (used simulate live feed to custom field acting as a counter)

Custom field ID and Jira issue showing custom field given as parameters.

** Usage:**

  -h, --help            show this help message and exit  
  -v                    Show version&author and exit  
  -w password           <JIRA password>  
  -u user               <JIRA user account>  
  -s server_address     <JIRA service>  
  -i jira_issue         <JIRA issue  
  -c customfieldname    <Customfield ID>  
  -l customfield_value  <Value for customfield>  
  -o on|off             <Execute small hardcoded (3 custom fields) livefeed simulator. Off by
                        default>  
  

  ** EXAMPLE: **
  
  
 *ChangeField.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -c CUSTOMFIELDID -v NUMBERVALUEFORCUSTOMFIELD -i JIRAISSUE*