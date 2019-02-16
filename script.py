#!/usr/bin/python
import json , dns.resolver, requests, sys ,random, pandas as pd
from termcolor import colored

slack_msg = ""
line = open('sites.txt').read().splitlines()

with open("servers.json") as f_in:
   data= json.load(f_in)
   
for i in data:
    
    site =random.choice(line)
    print("Testing:",i['dns_name'], i['ipaddress'], "to test:", site)
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = [i['ipaddress']]
    my_resolver.timeout     = 3
    my_resolver.lifetime    = 3
    
    try:
        answer = my_resolver.query(site)
        slack_msg= slack_msg +  "Server name = "  +  str(i['dns_name'])  +  " \t Server ip = "+str(i['ipaddress'])  +  " \t Status = Passed \n"
    except:
        print("Cannot Resolve hostname")
        slack_msg= slack_msg +  "`Server name = "  +  str(i['dns_name'])  +  " \t Server ip  = "+str(i['ipaddress'])  +  " Status = Failed` \n"

webhook_url = 'https://hooks.slack.com/services/***************************************************'
msg={'text': slack_msg }
try:
   requests.post(webhook_url,data=json.dumps(msg))
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
    sys.exit(1)
