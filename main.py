import webapp2
import logging
import json
import hmac
import hashlib
from email.utils import getaddresses, parseaddr

from google.appengine.api import mail, urlfetch


class HandleEmail(webapp2.RequestHandler):
    def post(self):
        # create email message and parse out fields
        message = mail.InboundEmailMessage(self.request.body)

        # list of emails: ['blah@example.com', ...]
        to = [addr[1] for addr in getaddresses([message.to])]
        cc = [addr[1] for addr in getaddresses([getattr(message, 'cc', '')])]

        sender = parseaddr(message.sender)[1]
        subject = getattr(message, 'subject', '')
        date = message.date

        html_body = ''
        for _, body in message.bodies('text/html'):
            html_body = body.decode()

        plain_body = ''
        for _, plain in message.bodies('text/plain'):
            plain_body = plain.decode()

        # Attachements are a list of tuples: (filename, EncodedPayload)
        # EncodedPayloads are likely to be base64
        #
        # EncodedPayload:
        # https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.mail#google.appengine.api.mail.EncodedPayload
        #
        attachments = []

        for attachment in getattr(message, 'attachments', []):
            encoding = attachment[1].encoding
            payload = attachment[1].payload

            if (not encoding or encoding.lower() != 'base64'):
                payload = attachment[1].decode().encode('base64')

            attachments.append({
                'filename': attachment[0],
                'payload': payload
            })

        # logging, remove what you find to be excessive
        logging.info('From <%s> to [<%s>]', sender,  '>, <'.join(to))
        logging.info('Subject: %s', subject)
        logging.info('Body: %s', plain_body)
        logging.info('Attachments: %s', [a['filename'] for a in attachments])

        # change to your endpoint (httpbin is cool for testing though)
        url = 'http://httpbin.org/post'

        payload = json.dumps({
          'sender': sender,
          'to': to,
          'cc': cc,
          'date': date,
          'subject': subject,
          'html_body': html_body,
          'plain_body': plain_body,
          'attachments': attachments
        })

        # add a key if you want to sign each request, or remove these lines
        key = 'XXXXXXXXXXXXXXXXXXXX'

        # hmac needs bytes (str() == bytes() in python 2.7)
        signature = hmac.new(
            bytes(key),
            bytes(payload),
            hashlib.sha1).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'X-Email-Signature': signature,
        }

        # try to post to destination
        try:
            result = urlfetch.fetch(
                url=url,
                headers=headers,
                payload=payload,
                method=urlfetch.POST)

            logging.info('POST to %s returned: %s', url, result.status_code)
            logging.info('Response body: %s', result.content)
        except urlfetch.Error as err:
            logging.exception('urlfetch error posting to %s: %s', url, err)


application = webapp2.WSGIApplication([
    ('/_ah/mail/.+', HandleEmail),
])
