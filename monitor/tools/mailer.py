from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import FileSystemLoader,Environment

from monitor.service.config import ConfigManager

import smtplib
import os

class MailSender(object):
    def __init__(self):
        self.config = ConfigManager.instance().getConfig()
        self.smtp_server = self.config.get("smtp", "server")
        self.smtp_port = int(self.config.get("smtp", "port"))
        self.smtp_user = self.config.get("smtp", "user")
        self.smtp_password = self.config.get("smtp", "password")
        self.smtp_from = self.config.get("smtp", "sendfrom")
        self.smtp_to = self.config.get("smtp", "sendto")
        self.mime_texts = []
        base_home = os.path.abspath(__file__)
        files_home = os.path.join(os.path.dirname(os.path.dirname(base_home)),"templates")
        LOADER = FileSystemLoader(files_home)
        self.ENV = Environment(loader = LOADER)

    def clear_mine_plain(self):
        self.mime_texts = []

    def add_mime_plain(self,message):
        self.mime_texts.append(MIMEText(message))

    def add_mime_html(self,template_name,**kwargs):
        template = self.ENV.get_template(template_name + '.jnj2')
        html_string = template.render(**kwargs)
        self.mime_texts.append(MIMEText(html_string,'html',_charset="utf-8"))

    def sendemail(self,subject):
        server = smtplib.SMTP(host=self.smtp_server,port=self.smtp_port)
        mime_count = len(self.mime_texts)
        if mime_count == 0:
            return
        if mime_count == 1:
            msg = self.mime_texts[0]
        else:
            msg = MIMEMultipart('Tethrnet')
            for mime_text in self.mime_texts:
                msg.attach(mime_text)

        msg['Subject'] = subject
        msg['From'] = self.smtp_from
        msg['To'] = self.smtp_to
        server.login(self.smtp_user,self.smtp_password)
        server.sendmail(self.smtp_from,self.smtp_to,msg.as_string())
        server.quit()
        logger.info("sendmail to %s for %s" % (self.smtp_to, subject))

if __name__ == '__main__':
    mailer = MailSender()
    mailer.add_mime_plain("Test")
    mailer.sendemail("Please ignore")