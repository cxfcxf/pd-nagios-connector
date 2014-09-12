# Pagerduty nagios connector

## only thing to change is the path to nagios.cmd

### step 1 
rename .ext to .cgi

### step 2
put file in your nagios cgi bin directory

### step 3
add a webhook to your service in pagerduty point to this link
```
httpauth webhook receiver
http://username:password@nagios.yourwebsite.com/nagios/cgi-bin/pd-nagios-connector.cgi
```

# future
more incident identifier from webhook will be written into function
