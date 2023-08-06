import smtplib as smtp
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText


class GenericMessage(MIMEMultipart):
    """Class used to construct messages that can be sent
    to port eail using a Sender instance.

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
        super().__init__(self)
        self['From'] = kwargs.get('origin')
        self['To'] = COMMASPACE.join(kwargs.get('destinys'))
        self['Subject'] = kwargs.get('title')
        self.preamble = kwargs.get('preamble', kwargs.get('title'))
        self.html = kwargs.get('html', None)
        self.content = kwargs.get('content', None)
        
        if self.html:
            self.attach(MIMEText(kwargs.get('html'), 'html'))
        
        if self.content:
            self.attach(MIMEText(kwargs.get('content'), 'plain'))
        
        for file in kwargs.get('attachments', []):
            with open(file, 'rb') as attachment:
                data = attachment.read()
                name = basename(file)
                part = MIMEApplication(data, name)
                part['Content-Disposition'] = f'attachment; filename="{name}"'
                self.attach(part)

class Sender:
    """Abstractions for send mails with SMTP.

    Arguments:
        SSL {bool} -- Indicates whether the connection to
                      the server should use SSL.
        TLS {bool} -- Indicates whether the connection to
                      the server should use TLS.
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
            self.server = smtp.SMTP_SSL(f'{self.host}: {str(self.port)}')

        else:
            self.server = smtp.SMTP(f'{self.host}: {str(self.port)}')

    def __enter__(self):
        self.load()
        
        if self.tls:
            self.server.starttls()

        self.server.ehlo()
        self.server.login(self.user, self.password)

        return self.server()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server:
            self.server.close()
