#!/usr/bin/env python
#written by sieg

import subprocess
import json
import sys
import time
import re

def checkackstatus(host, serv=""):
  with open("/usr/local/nagios/var/status.dat") as s:
    data = s.readlines()
    i = 0
    status = []
    for line in data:
      if re.search('{', line):
        start = i
      elif re.search('}', line):
        if serv == "":
          if re.search('hoststatus', data[start:i][0]) and re.search(host, data[start:i][1]):
            for ack in data[start:i]:
              if re.search('acknowledgement_type', ack):
                if ack.strip().split("=")[1] != "0":
                  return False
                else:
                  return True
        else:
          if re.search(host ,data[start:i][1]) and re.search(serv, data[start:i][2]):
            for ack in data[start:i]:
              if re.search('acknowledgement_type', ack):
                if ack.strip().split("=")[1] != "0":
                  return False
                else:
                  return True
      i = i + 1

cmd = "/usr/local/nagios/var/rw/nagios.cmd"

data = sys.stdin.read()
message = json.loads(data)

date = int(time.time())

for m in message["messages"]:
        if m["type"] == "incident.acknowledge":
                hostname = m["data"]["incident"]["trigger_summary_data"]["HOSTNAME"]
                service = m["data"]["incident"]["trigger_summary_data"]["SERVICEDESC"]
                username = m["data"]["incident"]["assigned_to_user"]["name"]

                if service == "":
                        if checkackstatus(hostname, ""):
                                subprocess.call("/bin/echo \"[%d] ACKNOWLEDGE_HOST_PROBLEM;%s;2;1;0;%s;acknowledged by nagctl\n\" > %s" % (date, hostname, username, cmd), shell=True)
                else:
                        if checkackstatus(hostname, service):
                                subprocess.call("/bin/echo \"[%d] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;2;1;0;%s;acknowledged by nagctl\n\" > %s" % (date, hostname, service, username, cmd), shell=True)


print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>MaxCDN pagerduty connector</title>'
print '</head>'
print '<body>'
print '<p>You are hitting MaxCDN pagerduty receiver</p>'
print '</body>'
print '</html>'
