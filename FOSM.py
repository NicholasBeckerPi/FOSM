__author__ = 'nicholove'

"FOSM script - File Organizer and Send Mail script"


import shutil
import os
from datetime import date
import re
import smtplib as sm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


if __name__ == '__main__':

    def action1():

        global archive_to_send

        def dir_verification():
            return os.path.exists('./ToBeZiped')

        directory = dir_verification()

        def make_dir():
            if not directory:
                try:
                    os.mkdir('./ToBeZiped')
                except OSError:
                    print('Creation error!')

        make_dir()

        def actual_day():
            now_run = str(date.today())
            res = re.compile(r'-')
            now_run = re.sub(res, '_', now_run)
            return now_run

        day_run = actual_day()

        def list_files():
            return list(os.listdir('./ToBeZiped'))

        def copy_files():
            try:
                shutil.copytree(src='./ToBeZiped', dst=f'./{day_run}' )
            except FileExistsError:
                pass

        def zip_files():
            return shutil.make_archive(f'{day_run}', 'zip', './ToBeZiped')

        print(f'The following archives will be copied: \n{list_files()}')

        archive_to_send = zip_files()
        zip_files()
        copy_files()


    def send_mail():
        # Setting user

        e_user = 'your_mail@gmail.com'
        e_receiver = 'othermail@gmail.com'
        password = 'password123'
        subject = 'FOSM HAS A MESSAGE!!'
        msg_body = 'Files organized and sent by FOSM'

        message = MIMEMultipart()
        message['From'] = e_user
        message['To'] = e_receiver
        message['Subject'] = subject

        message.attach(MIMEText(msg_body, 'plain'))

        filename = f'{archive_to_send}'
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename = {filename}")
        message.attach(part)
        text = message.as_string()

        # Sending mail
        server = sm.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(e_user, password)
        server.sendmail(e_user, e_receiver, text)
        server.quit()


    action1()
    send_mail()

