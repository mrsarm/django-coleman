from threading import Thread
from django.core.mail import send_mail


def send_mail_async(subject, message, from_email, recipient_list,
                     fail_silently=False, auth_user=None, auth_password=None,
                     connection=None, html_message=None):

    Thread(target=send_mail, args=(subject, message, from_email, recipient_list,
                                   fail_silently, auth_user, auth_password,
                                   connection, html_message)).start()
