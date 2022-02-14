#
# Emails configuration and templates used when a task order is created, CUSTOMIZE...
#

from . import env


EMAIL_TIMEOUT = 3      # seconds
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)
EMAIL_PORT = env.int('EMAIL_PORT', 587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', 'YOUREMAIL@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', 'PASS')

# Use 'django.core.mail.backends.console.EmailBackend'
# to use a fake backend that prints out the email
# in the standard output instead of sending the emails
EMAIL_BACKEND = env('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TASKS_SEND_EMAILS_TO_ASSIGNED = env.bool('TASKS_SEND_EMAILS_TO_ASSIGNED', False)
TASKS_SEND_EMAILS_TO_PARTNERS = env.bool('TASKS_SEND_EMAILS_TO_PARTNERS', False)


# Enables the Tornado Django Coleman Viewer (it will send emails with the order URL)
# Check: https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer
TASKS_VIEWER_ENABLED = env.bool('TASKS_VIEWER_ENABLED', False)
TASKS_VIEWER_HASH_SALT = env('TASKS_VIEWER_HASH_SALT', '1two3')   # REPLACE in production !!!
TASKS_VIEWER_ENDPOINT = env('TASKS_VIEWER_ENDPOINT', 'http://localhost:8888/{number}?t={token}')

MTASKS_EMAIL_WITHOUT_URL = '''\
New task #{id} created.

Title:
{title}

Assigned:
{user}

Description:
{description}

Please note: Do NOT reply to this email. This email is sent from an unattended mailbox.
Replies will not be read.

---
{sign}
'''


MTASKS_EMAIL_WITH_URL = '''\
New task #{id} created.

Title:
{title}

Assigned:
{user}

Description:
{description}

Order URL:
{url}

Please note: Do NOT reply to this email. This email is sent from an unattended mailbox.
Replies will not be read.

---
{sign}
'''
