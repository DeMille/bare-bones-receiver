import logging, email, urllib
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

class HandleEmail(InboundMailHandler):
    def receive(self, message):
        
        # Get Fields
        sender   = message.sender
        to       = message.to
        date     = message.date
        subject  = message.subject
        original = str(message.original)

        try :
            cc = message.cc
        except :
            cc = ''

        html_body = ''
        for content_type, body in message.bodies('text/html'):
            html_body = body.decode()
        
        for plain in message.bodies('text/plain'):
            plaintext_body = plain[1].decode()
        
        # Log stuff, comment some out if its too much for you
        logging.info('sender: ' + sender)
        logging.info('to: ' + to)
        logging.info('cc: ' + cc)
        logging.info('date: ' + date)
        logging.info('subject: ' + subject)
        logging.info('html_body: ' + html_body)
        logging.info('plaintext_body: ' + plaintext_body)
        logging.info('original: ' + original)

        # POST everything
        url = 'http://where ever you want <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
		
        form_fields = {
          'sender': sender.encode('utf8'),
          'to': to.encode('utf8'),
          'cc': cc.encode('utf8'),
          'date': date.encode('utf8'),
          'subject': subject.encode('utf8'),
          'html_body': html_body.encode('utf8'),
          'plaintext_body': plaintext_body.encode('utf8'),
          'original': original.encode('utf8')
        }

        form_fields = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url = url,
                                payload = form_fields,
                                method = urlfetch.POST,
                                headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'})
        logging.info('POST to ' + url + ' returned: ' + str(result.status_code))
        logging.info('Returned content: ' + result.content)


application = webapp.WSGIApplication([HandleEmail.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
