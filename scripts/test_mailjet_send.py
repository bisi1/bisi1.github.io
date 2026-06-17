#!/usr/bin/env python3
import json
import sys
import requests
from pathlib import Path

cfg_path = Path('api/sendEmail/local.settings.json.example')
if not cfg_path.exists():
    print('local settings example not found at', cfg_path)
    sys.exit(2)

cfg = json.loads(cfg_path.read_text())
vals = cfg.get('Values', {})
KEY = vals.get('MAILJET_API_KEY')
SECRET = vals.get('MAILJET_API_SECRET')
FROM_EMAIL = vals.get('FROM_EMAIL') or 'no-reply@yourdomain.com'
FROM_NAME = vals.get('FROM_NAME') or 'Virtuous IT'
TO_EMAIL = vals.get('TO_EMAIL') or ''

if not KEY or not SECRET:
    print('Mailjet API key/secret not configured in', cfg_path)
    sys.exit(2)

if not TO_EMAIL:
    print('TO_EMAIL not configured in', cfg_path)
    sys.exit(2)

subject = 'Test message from Virtuous IT site'
text = 'This is a test message sent from a local test script.'
html = '<p>This is a <strong>test</strong> message sent from a local test script.</p>'

payload = {
  "Messages": [
    {
      "From": {"Email": FROM_EMAIL, "Name": FROM_NAME},
      "To": [{"Email": TO_EMAIL, "Name": "Recipient"}],
      "Subject": subject,
      "TextPart": text,
      "HTMLPart": html
    }
  ]
}

print('Sending test email to', TO_EMAIL, 'via Mailjet...')
try:
    resp = requests.post('https://api.mailjet.com/v3.1/send', json=payload, auth=(KEY, SECRET), timeout=15)
    print('HTTP', resp.status_code)
    try:
        j = resp.json()
        # Print concise result
        if resp.ok:
            print('Mailjet accepted the message. Response summary:')
            print(json.dumps(j, indent=2)[:1000])
            sys.exit(0)
        else:
            print('Mailjet returned an error. Response:')
            print(json.dumps(j, indent=2))
            sys.exit(1)
    except Exception:
        print('Non-JSON response body; length:', len(resp.text))
        print(resp.text[:1000])
        sys.exit(1)
except requests.RequestException as e:
    print('Network error while contacting Mailjet:', str(e))
    sys.exit(1)
