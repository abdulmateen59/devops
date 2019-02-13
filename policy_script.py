import dns.resolver , requests , json
slack_msg = ""
blocked_ip='34.197.224.183'
safe_search_ip='216.239.38.120'


myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['45.74.47.1']    
try:
    myAnswers = myResolver.query("facebook.com", "A")
    for rdata in myAnswers: 
        ip=str(rdata)
	if(ip==blocked_ip):
		slack_msg= slack_msg + "Categeroy Policy Successful \n"
		print(ip)
	else:
		slack_msg=slack_msg + "Categeroy Policy Failed \n"
except dns.exception.DNSException as err:
    print("Query failed",err)

###################################################################################################################
myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['45.74.47.1']    
try:
    myAnswers = myResolver.query("twitter.com", "A")
    for rdata in myAnswers: 
        ip=str(rdata)
	if(ip!=blocked_ip):
		slack_msg= slack_msg + "Whitelist Policy Successful \n" 
                print(ip)
	else:
		slack_msg=slack_msg + "Whitelist Policy Failed \n"
except dns.exception.DNSException as err:
    print("Query failed",err)
###################################################################################################################
myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['45.74.47.1']    
try:
    myAnswers = myResolver.query("zigron.com", "A")
    for rdata in myAnswers: 
        ip=str(rdata)
	if(ip==blocked_ip):
		slack_msg= slack_msg + "Blacklist Policy Successful \n" 
		print(ip)
	else:
		slack_msg=slack_msg + "Blacklist Policy Failed \n"
except dns.exception.DNSException as err:
    print("Query failed",err)
####################################################################################################################
myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['45.74.47.1']    
try:
    myAnswers = myResolver.query("google.com", "A")
    for rdata in myAnswers: 
        ip=str(rdata)
	if(ip==safe_search_ip):
		slack_msg= slack_msg + "Safe search Policy Successful \n"
		print(ip)
	else:
		slack_msg=slack_msg + "Safe search Policy Failed \n" 
except dns.exception.DNSException as err:
    print("Query failed",err)
#####################################################################################################################
webhook_url = 'https://hooks.slack.com/services/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'
msg={'text': slack_msg }
try:
   requests.post(webhook_url,data=json.dumps(msg))
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
    sys.exit(1)
