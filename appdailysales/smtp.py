'''
Created on 02/11/2011
'''
import smtplib
from configuration import smtp_config
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate, COMMASPACE
from email.mime.text import MIMEText

def send_email(to, subject, body, attachments={}):
    server, usr, pwd, fromEmail = smtp_config()
    smtp = smtplib.SMTP(server)
    
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(usr, pwd)
    
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body))
    
    for name, at in attachments.iteritems():
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(at)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % name)
        msg.attach(part)
        
    smtp.sendmail(fromEmail, to, msg.as_string())
    smtp.quit()
