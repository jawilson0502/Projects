#!/usr/bin/python3

"""Script to parse through my website log to pull out valid visitors"""

import re
from IPython import embed

file_path = "access.log"

with open(file_path, "r") as f:
    log_file = f.read()

log_file = log_file.splitlines()

logs = []
ips = []
for log in log_file:
    print(log)
    fields = log.split()
    fields_dict = {}
    fields_dict['ip'] = fields[0]
    fields_dict['date'] = ' '.join(fields[3:5])
    fields_dict['rest'] = fields[5]
    fields_dict['page'] = fields[6]
    fields_dict['status_code'] = fields[8]
    fields_dict['referrer'] = fields[10]
    fields_dict['ua'] = ' '.join(fields[11:])
    
    ips.append(fields_dict['ip'])
    logs.append(fields_dict)

bad_ips = []
# Look for ips that only occur once, probs a bot
for ip in ips:
    if ips.count(ip) == 1:
        bad_ips.append(ip)

# Sort logs based on IP
logs.sort(key=lambda x: x['ip'])

# Uniq bad_ips
bad_ips = set(bad_ips)
i = 0
while i < len(logs):
        if logs[i]['ip'] in bad_ips:
            ips.remove(logs[i]['ip'])
            logs.remove(logs[i])
        else:
            i +=1

regex = "js|css|favicon|img|fonts"
good_ips = []
for log in logs:
    m1 = re.search(regex, log['page'])
    if m1:
        good_ips.append(log['ip'])

good_ips = set(good_ips)
i = 0
while i < len(logs):
    if logs[i]['ip'] not in good_ips:
        ips.remove(logs[i]['ip'])
        logs.remove(logs[i])
    else:
        i +=1
regex = """bot|proxy|seo|Synapse|scan|crawler|analytics|
        preview|speed|spider|button|facebookexternalhit|baidu"""
i = 0
while i < len(logs):
    try:
        m1 = re.search(regex, logs[i]['ua'], re.IGNORECASE)
        m2 = logs[i]['ua'] == "-"
        m3 = logs[i]["status_code"] == "400" or logs[i]["status_code"] == "403"
        # TODO: Add another conditional if it is not a GET or POST request
        if m1 or m2 or m3:
            ips.remove(logs[i]['ip'])
            logs.remove(logs[i])
        else:
            i += 1
    except:
        break
embed()
