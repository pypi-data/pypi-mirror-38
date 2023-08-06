import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import path
from enmailer.error import DataTypeError, InvalidEmailAddressError


class ENMailer:
    def __init__(self, **kwargs):
        """
        Make sure every parameter is in its correct data type:

        -----------------------------------------------------------------------
        VARIABLE    | Type | Description
        -----------------------------------------------------------------------
        dispatcher  | str  | Sender. This field is required to prevent error
        recipient   | str  | Evernote mail address
        title       | str  | Title of the note     | Optional (df: Untitled)
        contents    | str  | contents (plain text) | Optional (df: '')
        tags        | list | tags for the note     | Optional (df: None)
        notebook    | str  | saving notebook path  | Optional (df: None)
        SMTP_host   | str  | SMTP host             | Optional (df: 'localhost')
        SMTP_port   | int  | SMTP port             | Optional (df: 25)
        attachments | list | fpath for attachments | Optional (df: [])
        -----------------------------------------------------------------------

        """
        self._subject = kwargs.get('title', None)
        self._dispatcher = kwargs.get('dispatcher', None)
        self._recipient = kwargs.get('recipient', None)
        self._contents = kwargs.get('contents', "")
        self._tags = kwargs.get('tags', [])
        self._notebook = kwargs.get('notebook', None)
        self._SMTP_host = kwargs.get('SMTP_host', 'localhost')
        self._SMTP_port = kwargs.get('SMTP_port', 25)
        self._attachments = kwargs.get('attachments', [])
        self._contents_type = 'plain'

    def send(self):
        """
        This method sends email via SMTP. By default, it uses port 25 and runs
        on localhost, meaning that sendmail should have been installed as a
        prerequisite.

        Please take a look at README.md for further installation guidelines.
        """

        # Check if every value is set in correct data format:
        self.confirm()

        # Create message object:
        message = MIMEMultipart()
        message['From'] = self._dispatcher
        message['To'] = self._recipient

        # (Notebook path and tags are managed via title settings:)
        title = [self._subject]
        title.append('@' + self._notebook) if self._notebook else None
        title += list(" #" + tag for tag in self._tags)
        message['Subject'] = "".join(title)

        # Add body:
        body = self._contents
        message.attach(MIMEText(body, self._contents_type))

        # Update header if any file attachment has been made:
        for filepath in self._attachments:
            filename = path.basename(filepath)
            fp = open(filepath, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((fp).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename= {}'.format(filename))

            message.attach(part)

        # Send mail via local `sendmail` using `self._SMTP_port`
        server = smtplib.SMTP(self._SMTP_host, self._SMTP_port)
        server.sendmail(self._dispatcher,
                        self._recipient, message.as_string())
        server.quit()

    def confirm(self):
        """
        This method confirms the settings prior to actual request of the
        mail.
        """

        # Check if recipient and dispatcher are in correct email form:
        if type(self._recipient) is not str:
            raise DataTypeError('recipient', 'str')
        if len(self._recipient.split('@')) != 2:
            raise InvalidEmailAddressError(self._recipient, 'recipient')

        if type(self._dispatcher) is not str:
            raise DataTypeError('dispatcher', 'str')
        if len(self._dispatcher.split('@')) != 2:
            raise InvalidEmailAddressError(self._dispatcher, 'dispatcher')

        # Check other optional values:
        if type(self._subject) is not str:
            raise DataTypeError('title', 'str')
        if type(self._contents) is not str:
            raise DataTypeError('contents', 'str')
        if type(self._tags) is not list:
            raise DataTypeError('tags', 'list')
        for item in self._tags:
            if type(item) != str:
                raise DataTypeError('tag', 'str')
        if type(self._notebook) is not str and self._notebook is not None:
            raise DataTypeError('notebook', 'str')
        if type(self._SMTP_host) is not str:
            raise DataTypeError('SMTP_host', 'str')
        if type(self._SMTP_port) is not int:
            raise DataTypeError('SMTP_port', 'int')

        # Check contents_type:
        if self._contents_type not in ('plain', 'html'):
            raise DataTypeError('contents_type', "('plain', 'html')")


###############################################################################
    # Below are methods that manually changes the settings:

    def attach(self, filepath):
        """ Attach a file """
        self._attachments.append(filepath)

    def add_tag(self, tag):
        """ Add a tag"""
        self._tags.append(tag)

    def set_notebook(self, notebook):
        """ Set notebook saving path """
        self._notebook = notebook

    def set_recipient(self, recipient):
        """Set Recipient of the note """
        self._recipient = recipient

    def set_dispatcher(self, dispatcher):
        """Set dispatcher(a.k.a. sender) of the note """
        self._dispatcher = dispatcher

    def set_title(self, title):
        """ Set title of the note """
        self._subject = title

    def write_text(self, contents):
        """ Write contents in plain text """
        self._contents = contents
        self._contents_type = 'plain'

    def write_html(self, contents):
        """ Write contents in html or ENML """
        self._contents = contents
        self._contents_type = 'html'
