import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'sguzch@163.com'
reciveer = 'sguzch@163.com'
subject = '放假通知'
smtpserver = 'smtp.163.com'
username = 'sguzch@163.com'
password = 'wywywywy2013'

msg = MIMEText('Spring Fastval', 'plain', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = 'zhengch<sguzch@163.com>'
msg['To'] = reciveer
smtp=smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, reciveer, msg.as_string())
smtp.quit()