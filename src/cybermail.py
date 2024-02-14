# coding=utf-8

from __future__ import unicode_literals
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class EmailAPI(object):
    def connect(self, loc):
        self.server = SMTP(
			loc)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(
			C.EMAIL, 
			C.EMAIL_PW)
        self.msg = MIMEMultipart(
			'alternative')
    def send_to(self, email):
        self.msg['To'] = email
    def subject(self, subject):
        self.msg['Subject'] = subject
    def send_from(self, email):
        self.msg['From'] = email
    def serve(self, html):
        mime = MIMEText(
			html, 'html', 'utf-8'
			)
        self.msg.attach(mime)
        msg_str = self.msg.as_string()
        self.server.sendmail(
			self.msg['From'], 
			self.msg['To'],
			msg_str)
        self.server.quit()

class Email(EmailAPI):
    def __init__(self):
        super(Email, self).__init__()
    def send(self, html):
        self.subject(
			Snippet(
				'Message From ',
				self.msg['From']
				).string()
			)
        self.serve(html)

class GMail(Email):
	def __init__(self):
		super(
			GMail, 
			self
			).__init__()
		self.connect(
			'smtp.gmail.com:587'
			)