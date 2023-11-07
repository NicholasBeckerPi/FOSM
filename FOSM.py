__author__ = 'nicholove'

import shutil
import os
from datetime import date
import re
import smtplib as sm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Teste GIT push

class Computer:
    def __init__(self, file_path):
        self.file_path = file_path

    def path_verification(self):
        if not os.path.exists(self.file_path):
            print('ATENÇÃO! ESTE DIRETÓRIO NÃO EXISTE!')
            return inputs()
        else:
            pass

    # Retorna a pasta com o dia
    @staticmethod
    def actual_day():
        now_day = str(date.today())
        res = re.compile(r'-')
        now_run = re.sub(res, '_', now_day)
        return now_run

    # Copia para a pasta do dia
    def copy_files(self):
        try:
            shutil.copytree(src=f'./{self.file_path}', dst=f'./{Computer.actual_day()}')
        except FileExistsError:
            pass

     # Lista os arquivos que serão copiados
    @staticmethod
    def list_files():
        return list(os.listdir(f'{Computer.actual_day()}'))

    # Cria um zip da pasta do dia
    @staticmethod
    def zip_files():
        return shutil.make_archive(f'{Computer.actual_day()}', 'zip', f'./{Computer.actual_day()}')



class EmailSender:
    def __init__(self, user_address, receiver_address, password, subject, body_message):
        self.user_address = user_address
        self.receiver_address = receiver_address
        self.password = password
        self.subject = subject
        self.body_message = body_message

    def setting_mail(self):  # Prepara o email para ser enviado
        global text
        message = MIMEMultipart()
        message['From'] = self.user_address
        message['To'] = self.receiver_address
        message['Subject'] = self.subject
        message.attach(MIMEText(self.body_message, 'plain'))
        filename = f'{Computer.actual_day()}.zip'
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename = {filename}")
        message.attach(part)
        text = message.as_string()

    def sending_mail(self):  # Envia o email
        server = sm.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.user_address, self.password)
        server.sendmail(self.user_address, self.receiver_address, text)
        server.quit()


def inputs():
    path = input('Caminho do arquivo: ')
    c1 = Computer(path)
    c1.path_verification()
    user_address = input('Seu email: ')
    receiver_address = input('Destinatário: ')
    password = input('Sua senha: ')
    subject = input('Assunto: ')
    body_message = input('Texto de corpo: ')

    def run():
        c1.actual_day()
        c1.copy_files()
        c1.list_files()
        c1.zip_files()
        e1 = EmailSender(user_address, receiver_address, password, subject, body_message)
        e1.setting_mail()
        e1.sending_mail()
    return run()


if __name__ == '__main__':
    inputs()



