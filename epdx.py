import os, pwd, grp, smtplib, time, subprocess
from time import strptime
from datetime import datetime
from email.mime.text import MIMEText

def log(value):
        message = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " +  str(value)
        os.system("echo '"+str(message)+"' >> ./epdx.log")

def send_email(message):
    try:
        recipients = [""]
        subject = "Expired Password Detected"
        body = str(message)
        sender = "SENDER EMAIL ADDRESS"
        password = "GOOGLE API KEY"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        log("INFO: ALERT MESSAGE RECIPIENTS: " + str(recipients))
    except:
        log("ERROR: SOMETHING HAPPENED WHEN EMAIL MODULE TRIGGERED!, EMAIL DIDNT SEND!")

def getUsers():
    userList = []
    for user in pwd.getpwall():
        userList.append(user[0])
    return userList


def main():
    os.system("clear")
    lastLine = None
    message = "Service EPDx Started!"
    header = "EPDx Info"

    while True:
        userList = getUsers()
        with open('/var/log/auth.log','r') as f:
            lines = f.readlines()
        if lines[-1] != lastLine:
            lastLine = lines[-1]

            if 'expired password for user' in lines[-1]:
                for user in userList:
                    if user in lines[-1]:
                        header = "Expired Password Detected - Server: Test Vpn"
                        message = str(user) +"'s Password Expired At " + str(lines[-1].split(':')[0])
                        log("WARNING:" + message)
            send_email(header, message)

        time.sleep(10)

main()
