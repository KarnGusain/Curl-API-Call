#!/home/user1/Karn_python3/bin/python
#########################################################################################
### Title: Generate report from HPE Global Dashboard in CSV format                    ###
### Version: 01                                                                       ###
### Published: 13th December 2020                                                     ###
### Author: Karn Kumar (karn.itguy@gmail.com)                                           ###
### Usage: python hpe_OneView_Report.py                                               ###
#########################################################################################
import pandas as pd
pd.set_option('expand_frame_repr', True)
########################################################################################
## Importing SMTP for the e-mail distribution                                        ###
########################################################################################
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from smtplib import SMTP
import subprocess
import glob
#########################################################################################
# Below Subprocess call will excecute the Shell Script and generates file to          ###
# the "/home/user1/script_logs/" which further will be used with Pandas python lib    ###
# Panda will be Extracting raw comma delimited files as csv and converting to HTML    ###
#########################################################################################
subprocess.call(['sh', 'collect_hpe_alerts.sh'])
# Using glob here as we have some metachars in file name before ".csv"
for file in glob.glob("/home/user1/script_logs/hpeCriticalAlert*.csv"):
   df = pd.read_csv(file)
#
recipients = ['abc@example.com', 'xyz@example.com']
mail_receivers = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = "HTML OneView"
msg['From'] = 'yourEMailaddress@example.com'
#################################################################
# HTML OUTLOOK BODY                                             #
#################################################################
html = """\
<html>
  <head>
  <style>
  table, th, td {{font-size:9pt; border:1px solid black; border-collapse:collapse; text-align:left; background-color:LightGray;}}
  th, td {{padding: 5px;}}
  </style>
  </head>
  <body>
     Dear Team,<br><br>
     Please Find the HP OneView Alert Report Below and kindley act accordingly!<br><br>
     {0} <br><br>
    Kind regards.<br>
    HPE Global Dashboard.
  </body>
</html>
  """.format(df.to_html(index=False))

part1 = MIMEText(html, 'html')
msg.attach(part1)

server = smtplib.SMTP('your_smtp_server')
server.sendmail(msg['From'], mail_receivers, msg.as_string())
