# Bare Bones Receiver

This is a Google App Engine app that receives emails and POSTs them as JSON to a url. It's an easy way to add incoming mail to a web app.

The goal is to enable this chain of email forwarding:
<br/>
something<span></span>@yourdomain.com 🡒 receiver<span></span>@your-app.appspotmail.com 🡒 yourdomain.com/handle_email

The receiver is python but it **requires** app engine because it uses the platform to get the incoming mail.


### How to use

There isn't much setup to this, just change a thing or two and upload. You can look at the [getting started](https://cloud.google.com/appengine/docs/standard/python/quickstart) page to see more details about how to use app engine, but the basics for this project will be:
- Create a new app engine project
- Download the google cloud sdk (if you don't have it)
- `git clone https://github.com/DeMille/bare-bone-receiver.git`
- Change the `url` in `main.py` to your endpoint, tweak whatever
- `gcloud app deploy app.yaml`

The receiver will forward any incoming mail that matches: `__________@<your-app-id>.appspotmail.com` to your url.

If you want to use your own domain, tell your registrar to forward emails from your domain (either from a specific address or from a catch-all address) to a receiver address (`__________@<your-app-id>.appspotmail.com`). You can use any `__________@` you want since the receiver will handle all addresses.

\*\***NOTE**\*\* <br/>
**Don't forget the appspot<span></span>_MAIL_ part of the email address!  It won't get delivered without it.**


### What requests looks like
Requests are sent as POSTs with `Content-Type: application/json`:

```JSON
{
  "sender": "tom@example.com",
  "to": ["alex@example.com"],
  "cc": ["elisha@example.com"],
  "date": "Fri, 10 Mar 1876 15:54:49 -0500",
  "subject": "Urgent!",
  "html_body": "&lt;html&gt;&lt;div dir=\"ltr\"&gt;Mr. Watson, come here — I want to see you.&lt;/div&gt;&lt;/html&gt;",
  "plain_body": "Mr. Watson, come here — I want to see you.",
  "attachments": [
    {
      "filename": "example.txt",
      "payload": "baWEfsdv25DF654... base64"
    }
  ]
}
```

- `to` and `cc` are always lists, even with only 1 or no addresses
- `plain_body` is just the plain text version of `html_body`
- attachments payloads are base64 encoded


###  Verifying requests
To verify that requests are coming from your receiver and not some malicious third party you can check the signature generated for each request. HMAC-SHA1 signatures are created using a secret key and the body of the request. They are included in the request header under `X-Email-Signature` as a hex digest.

At your endpoint you can compute the signature using your secret key and compare it to the one in the request header to know if the request is valid. In python, for example, you could do this like:
```python
import hmac
import hashlib

header = headers.getheader('X-Email-Signature')
signature = hmac.new(bytes(key), bytes(request.body), hashlib.sha1).hexdigest()

hmac.compare_digest(header, signature) # True/False
```

If you want these signatures you need to add your own `key` in `main.py`. (As an aside, I don't know how to include secret keys in app engine projects without hard coding them _somewhere_. So if you have a better idea, do that instead.)


###  Notes

- You can define the email address(es) that will receive email in your `app.yaml`. The given configuration will match _any_ email addresses at your appspotmail subdomain.  See the [docs](https://cloud.google.com/appengine/docs/standard/python/mail/receiving-mail-with-mail-api) if you want to define different / multiple handlers.

- Google app engine has [limits](https://cloud.google.com/appengine/docs/standard/python/outbound-requests#quotas_and_limits) on outgoing request sizes (10mb request and 32mb response).

- The main pricing items you'll want to pay attention to (depending on how much email you process) are instance hours and outgoing bandwidth. ([pricing page](https://cloud.google.com/appengine/pricing))


### License

The MIT License (MIT)

Copyright (c) 2014 Sterling DeMille

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.