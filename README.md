# Bare Bones Receiver

This is a simple Google App Engine app that will receive emails and POST them to a url.
It's a cheap and easy way to let your app receive emails without having to deal with email server madness.

## How to use

There shouldn't be much setup to this, just change a thing or two and upload:
- Fire up a new GAE app
- Change the `application` in app.yaml to your app id
- Change the `url` in main.py to your POST endpoint
- Deploy!

Any emails following this format are received and forwarded to your specified endpoint: __________@\<your-app-id\>.appspotmail.com

Dont forget the appspot _MAIL_ part!  Otherwise it won't go through.

## POST parameters

- `sender`: sender's email address, e.g. `Nobody <nobody@example.com>`
- `to`: comma separated list, e.g. `Joe <joe@example.com>, Bill <bill@example.com>`
- `cc`: comma separated list like, may or may not exist
- `date`
- `subject`
- `html_body`: may or may not exist
- `plain_body`
- `attachments`: a JSON list of any attachments, following this form:

```JSON
{
    "filename": "filename.ext",
    "encoding": "base64",
    "payload": "iVBORw0KGgoAAAANSUhEUgAAAyAAAAJYCAIAA..."
}
```


## Notes

- You can define the email address(es) that will receive email in you `app.yaml`. The given configuration will match _any_ email addresses at your appspotmail subdomain.  See the [docs](https://cloud.google.com/appengine/docs/python/mail/receivingmail) if you want to define different / multiple handlers.

- Google app engine has [limits](https://cloud.google.com/appengine/docs/python/urlfetch/#Python_Quotas_and_limits) on request sizes (10mb request and 32mb response). If you are using this with attachments you might want to make sure you understand all of the quotas and limits on the platform.