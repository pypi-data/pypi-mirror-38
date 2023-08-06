# MailMe

Library created to abstract work with SMTP servers to send e-mails.

## Install

To install the library use the command `pip install mailme`.


## Comments

- For a characteristic of the library, when informing when passing
'content' and 'html' as parameters of a message, both will be
inserted in the body of the same, being first displayed the content
and then the html, always in that order.

- Attachments and recipients should always be informed in list form,
even if we only have one string inside it.

- The library is in constant development. If you believe something
can improve, feel free to open an echo or do a poll request.

- The library was developed over python 3.7 and can not guarantee 
its backward compatibility.