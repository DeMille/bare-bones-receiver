# Bare Bones Receiver

This is a simple Google App Engine app that will receive emails and POST them to a url.
It's a cheap and easy way to let your app receive emails.

## How to use it

There shouldn't be much setup to this, just change a thing or two and upload:
- Fire up a new GAE app
- Change the 'application' in app.yaml to your app name
- Change 'url' in main.py to your POST url
- Deploy!

## POST format

The POST output is like the one described in the GAE mail docs [here](https://developers.google.com/appengine/docs/python/mail/receivingmail)

sender         : The message sender
to             : Sent to
cc             : Cc
date           : Date
subject        : Subject
html_body      : HTML version of the body
plaintext_body : Plain text version of the body
original       : The original message, complete with email headers and attachments, ect

If you want to attachments just use your preferred method to parse them out of the original once you receive the POST at your url. (Unless you can find a better way to send multipart POST from the attachments, I couldn't seem to find a good way to do it.)