import smtplib as smtp
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText

import magic as mime


class Message:
    """Class used to construct messages that can be sent to port
    email using a Sender instance.
    
    Arguments:
        origin {str} -- Who is sending the message.
        destinys {List} -- List with the recipients of the message.
        title {str} -- Message subject.
        content {str} --  Body of the message itself.
        preamble {str} -- Summary of the message to be sent.
        html {str} -- Message to be displayed in HTML format.
        attachments {List} -- List with the patch all files to be attached.
    """

    def __init__(self, *args, **kwargs):
        self.origin = kwargs.get('origin')
        self.destinys = kwargs.get('destinys')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.attachments = kwargs.get('attachments', [])
        self.preamble = kwargs.get('preamble', self.title)
        self.html = kwargs.get('html', None)
        self.plain = MIMEMultipart()

    def parse(self):
        """Loads an MIMEMultipart instance with all the information
        configured in instantiation of this class.
        
        Returns:
            message [MIMEMultipart] -- An instance of MIMEMultipart already worked.
        """

        self.plain['From'] = self.origin
        self.plain['To'] = COMMASPACE.join(self.destinys)
        self.plain['Subject'] = self.title
        self.plain['Date'] = formatdate(localtime=True)
        self.plain.preamble = self.title
        
        if self.content:
            self.plain.attach(MIMEText(self.content, 'plain'))

        for file in self.attachments:
            with open(file, 'rb') as attachment:
                data = attachment.read()
                name = basename(file)
                part = MIMEApplication(data, name)
                part['Content-Disposition'] = f'attachment; filename="{name}"'
                self.plain.attach(part)
        
        if self.html:
            self.plain.attach(MIMEText(self.html, 'html'))

        return self.plain

class Sender:
    """Abstractions for send mails with SMTP.
    
    Arguments:
        SSL {bool} -- Indicates whether the connection to the server should use SSL.
        TLS {bool} -- Indicates whether the connection to the server should use TLS.
        host {str} -- Connection address with SMTP server.
        port {int} -- Port connection to the SMTP server.
        user {str} -- Username to authenticate to any SMTP server.
        password {str} -- Password to authenticate to any SMTP server.
    """

    def __init__(self, *args, **kwargs):
        self.ssl = kwargs.get('SSL', False)
        self.tls = kwargs.get('TLS', False)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.server = None

    def load(self):
        """Establish the connection to the SMTP server according to the
        settings you have entered.
        """
        if self.ssl:
            self.server = smtp.SMTP_SSL(self.host, self.port)

        else:
            self.server = smtp.SMTP(self.host, self.port)


    def send(self, message):
        """Function used to trigger messages from the configured server.
        
        Arguments:
            message {Message} -- An instance of mailme.Message.
        """
        if isinstance(message, Message):
            self.server.send_message(message.parse())

    def __enter__(self):
        self.load()
        self.server.ehlo()
        self.server.login(self.user, self.password)

        if self.tls:
            self.server.starttls()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server:
            self.server.close()
