import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email(your_addr, addressee, your_passwd, subject, message):
    ''' Addressee can be more than one '''
    class Exceptions(Exception):
    ''' Base class exception for email '''
    pass
    class AuthenticationError(Exceptions):
        ''' Address could not be found or password is incorrect '''
        pass
    class RuntimeError(Exceptions):
        ''' A problem occured in the process of sending email '''
        pass
    class DomainError(Exceptions):
        ''' Invalid domain/ domain unable to be recognized '''
        pass

    valid_address_code = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
    valid_addressees = re.finditer(valid_address_code, addressee)
    
    valid_address = re.match(valid_address_code, your_addr)
    msg = MIMEMultipart()
    msg['From'] = your_addr
    msg['To'] = addressee
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    
    if valid_address:
        if your_addr.endswith('@gmail.com'):
            server = smtplib.SMTP('smtp.gmail.com', 587)
        elif your_addr.endswith('@yahoo.com'):
            server = smtplib.SMTP('smtp.mail.yahoo.com', 465)
        elif your_addr.endswith('@outlook.com') or your_addr.endswith('@hotmail.com') or your_addr.endswith('@live.com'):
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        else:
            raise DomainError('Domain is not recognizable')
    else:
        raise AuthenticationError("Invalid address format")

    server.starttls()
    try:
        server.login(your_addr, your_passwd)
    except:
        raise AuthenticationError('Incorrect password')
    else:
        text = msg.as_string()
    try:
        server.sendmail(your_addr, addressee, text)
    except:
        raise RuntimeError("Addressee/s couldn't be found")
    server.quit()
            
    
    
