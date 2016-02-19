import requests
import smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText

config = ConfigParser()
config.read(['littlefield.ini'])


def send(text, subject="Littlefield Update"):
    if 'debug' in config['mail']:
    message = MIMEText(text)
    message['Subject'] = subject
    message['From'] = config['mail']['from']
    message['To'] = config['mail']['to']

    s = smtplib.SMTP(config['mail']['server'], 587)
    s.starttls()
    s.login(config['mail']['user'], config['mail']['password'])
    s.sendmail(config['mail']['from'], config['mail']['to'].split(" "), message.as_string())
    s.quit()
