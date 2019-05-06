import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from partner.models import Partner
from coleman.utils.mail import send_mail_async as send_mail
from hashlib import sha1


logger = logging.getLogger(__name__)

number_tr = _("number")


class Task(models.Model):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )

    PRIORITIES = (
        ('00_low', _('Low')),
        ('10_normal', _('Normal')),
        ('20_high', _('High')),
        ('30_critical', _('Critical')),
        ('40_blocker', _('Blocker'))
    )

    title = models.CharField(_("title"), max_length=200)
    partner = models.ForeignKey(Partner, blank=True, null=True, on_delete=models.PROTECT)
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.number, self.title)

    @property
    def number(self):
        return "{:08d}".format(self.pk)

    def save(self, *args, **kwargs):
        task_created = self.pk is None
        super().save(*args, **kwargs)
        if task_created:
            self.send_new_task_email()

    def send_new_task_email(self):
        """
        Override with a custom email
        """
        emails_to = []
        if settings.TASKS_SEND_EMAILS_TO_PARTNERS and getattr(self, "partner", None) and self.partner.email:
            emails_to.append(self.partner.email)
        if settings.TASKS_SEND_EMAILS_TO_ASSIGNED and getattr(self, "user", None) and self.user.email:
            emails_to.append(self.user.email)
        if len(emails_to):
            logger.info("[Task #%s] Sending task creation email to: %s", self.number, emails_to)
            vals = {
                "id": self.number,
                "user": str(self.user) if getattr(self, "user", None) else '(Not assigned yet)',
                "title": self.title,
                "description": self.description or '-',
                "sign": settings.SITE_HEADER,
            }
            if settings.TASKS_VIEWER_ENABLED:
                email_template = settings.MTASKS_EMAIL_WITH_URL
                vals["url"] = self.get_tasks_viewer_url()
            else:
                email_template = settings.MTASKS_EMAIL_WITHOUT_URL
            try:
                send_mail(
                    '[{app}] [#{id}] New Task Created'.format(app=settings.APP_NAME, id=self.number),
                    email_template.format(**vals),
                    settings.APP_EMAIL,
                    emails_to,
                )
            except Exception as e:
                logger.warning("[Task #%s] Error trying to send the task creation email - %s: %s",
                               self.number, e.__class__.__name__, str(e))

    def get_tasks_viewer_url(self):
        """
        Verification token added to the Tasks Viewer URL so each one
        sent through email cannot be used to change the order number and
        access to other orders.

        It uses as input a salt code and
        some immutables fields from the order (the ID number and
        the date the order was created)

        See: coleman/settings_emails.py
             https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer
        """
        salt = settings.TASKS_VIEWER_HASH_SALT
        if not settings.DEBUG and salt == '1two3':
            logger.warning("Insecure salt code used to send email orders, do NOT use it in PRODUCTION")
        created_at_as_iso = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")   # This ISO format is the same used
                                                                                # used by the REST serializer
        token = "{}-{}-{}".format(salt, self.pk, created_at_as_iso)             # SHA-1 is enough secure for
        token = sha1(token.encode('utf-8')).hexdigest()                         # this purpose (SHA-2 is too long)
        return settings.TASKS_VIEWER_ENDPOINT.format(number=self.number, token=token)

class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Check List")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(_("description"), max_length=200)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return self.item_description
