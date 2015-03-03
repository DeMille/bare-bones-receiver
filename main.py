import webapp2
import logging
import urllib
import json

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import urlfetch


class HandleEmail(InboundMailHandler):
    def receive(self, message):

        # parse out fields
        to = message.to
        sender = message.sender
        cc = getattr(message, 'cc', '')
        date = message.date
        subject = message.subject

        # Original message, as a python email.message.Message
        # original = str(message.original)

        html_body = ''
        for _, body in message.bodies('text/html'):
            html_body = body.decode()

        plain_body = ''
        for _, plain in message.bodies('text/plain'):
            plain_body = plain.decode()

        # Attachements are EncodedPayload objects, see
        # https://code.google.com/p/googleappengine/source/browse/trunk/
        # python/google/appengine/api/mail.py#536
        attachments = [{
                        'filename': attachment[0],
                        'encoding': attachment[1].encoding,
                        'payload': attachment[1].payload
                       }
                       for attachment
                       in getattr(message, 'attachments', [])]

        # logging, remove what you find to be excessive
        logging.info('sender: %s', sender)
        logging.info('to: %s', to)
        logging.info('cc: %s', cc)
        logging.info('date: %s', date)
        logging.info('subject: %s', subject)
        logging.info('html_body: %s', html_body)
        logging.info('plain_body: %s', plain_body)
        logging.info('attachments: %s', [a['filename'] for a in attachments])

        # POST (change to your endpoint, httpbin is cool for testing though)
        url = 'http://httpbin.org/post'

        form_fields = urllib.urlencode({
          'sender': sender.encode('utf8'),
          'to': to.encode('utf8'),
          'cc': cc.encode('utf8'),
          'date': date.encode('utf8'),
          'subject': subject.encode('utf8'),
          'html_body': html_body.encode('utf8'),
          'plain_body': plain_body.encode('utf8'),
          'attachments': json.dumps(attachments)
        })

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }

        result = urlfetch.fetch(url=url,
                                method=urlfetch.POST,
                                payload=form_fields,
                                headers=headers)

        # log more
        logging.info('POST to %s returned: %s', url, result.status_code)
        logging.info('Returned content: %s', result.content)

application = webapp2.WSGIApplication([HandleEmail.mapping()], debug=True)
