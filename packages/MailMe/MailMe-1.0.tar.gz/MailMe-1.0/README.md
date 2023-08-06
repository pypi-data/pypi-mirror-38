# MailMe

Library created to abstract work with SMTP servers to send e-mails.

## Settings

All settings must be made explicitly in the code (see examples).
Below is a table with the parameters of each of the two main classes:

### Sender

| Parameter |   Type  | Required |                           Description                          |
|:---------:|:-------:|:--------:|:--------------------------------------------------------------:|
|    SSL    | Boolean |    No    | Indicates whether the connection to the server should use SSL. |
|    TLS    | Boolean |    No    | Indicates whether the connection to the server should use TLS. |
|    host   |  string |    yes   |              Connection address with SMTP server.              |
|    port   | integer |    yes   |               Port connection to the SMTP server.              |
|    user   |  string |    yes   |          Username to authenticate to any SMTP server.          |
|  password |  string |    yes   |          Password to authenticate to any SMTP server.          |

### Message

|  Parameter  |     Type     | Required |                  Description                  |
|:-----------:|:------------:|:--------:|:---------------------------------------------:|
|    origin   |    string    |    yes   |          Who is sending the message.          |
|   destinys  | List[string] |    yes   |    List with the recipients of the message.   |
|    title    |    string    |    yes   |                Message subject.               |
|   content   |    string    |    no    |          Body of the message itself.          |
|   preamble  |    string    |    no    |       Summary of the message to be sent.      |
| attachments | List[string] |    no    | List with the patch all files to be attached. |

## Example

Below you can see how to forward an email with a few lines of code:

### Sending a simple email
```python
from mailme import Message, Sender

gmail = {'SSL': True,
         'host': 'smpt.gmail.com',
         'port': 465,
         'user': 'vitor.hov@gmail.com',
         'password': 'password'}

message = {'origin': 'vitor.hov@gmail.com',
           'destinys': ['destiny@example.com'],
           'title': 'This is an example',
           'content': 'This is a sample message.',
           'attachments': ['/path/to/illuminatis.png']}

if __name__ == '__main__':
    with Sender(**gmail) as server:
        message = Message(**data)
        server.send(message)
```

### Sending an email with HTML

Imagine a file 'file.html' with the following content:
```
<html>
    <head></head>
    <body>
        <h1>Title</h1>
        <p>A Whatever content.</p>
    </body>
</html>
```

The python code would look something like:

```python
from mailme import Message, Sender

with open('/path/to/file.html', 'r') as file:
    html = file.read()

gmail = {'SSL': True,
         'host': 'smpt.gmail.com',
         'port': 465,
         'user': 'vitor.hov@gmail.com',
         'password': 'password'}

message = {'origin': 'vitor.hov@gmail.com',
           'destinys': ['destiny1@example.com',
                        'destiny2@example.com'],
           'title': 'This is an example',
           'html': html}

if __name__ == '__main__':
    with Sender(**gmail) as server:
        message = Message(**data)
        server.send(message)
```

## Comments

- For a characteristic of the library, when informing when passing
'content' and 'html' as parameters of a message, both will be
inserted in the body of the same, being first displayed the content
and then the html, always in that order.

- Attachments and recipients should always be informed in list form,
even if we only have one string inside it.

- The library is in constant development. If you believe something
can improve, feel free to open an echo or do a poll request.