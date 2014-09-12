#!/usr/bin/env python
#written by sieg

import subprocess
import json
import sys
import time

cmd = "/path/to/nagios.cmd"

data = sys.stdin.read()
message = json.loads(data)

date = int(time.time())

for m in message["messages"]:
        if m["type"] == "incident.acknowledge":
                hostname = m["data"]["incident"]["trigger_summary_data"]["HOSTNAME"]
                service = m["data"]["incident"]["trigger_summary_data"]["SERVICEDESC"]
                username = m["data"]["incident"]["assigned_to_user"]["name"]

                if service == "":
                        subprocess.call("/bin/echo \"[%d] ACKNOWLEDGE_HOST_PROBLEM;%s;2;1;0;%s;acknowledged by nagctl\n\" > %s" % (date, hostname, username, cmd), shell=True)
                else:
                        subprocess.call("/bin/echo \"[%d] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;2;1;0;%s;acknowledged by nagctl\n\" > %s" % (date, hostname, service, username, cmd), shell=True)


print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>pagerduty connector</title>'
print '</head>'
print '<body>'
print '<p>You are hitting pagerduty connector</p>'
print '</body>'
print '</html>'
