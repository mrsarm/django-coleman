import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from partner.models import Partner
from django.core.mail import send_mail


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
            #  TODO: This is blocking call, it should be translated to an
            #        asyncronous version
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
            try:
                send_mail(
                    '[{app}] [#{id}] New Task Created'.format(app=settings.APP_NAME, id=self.number),
                    '''\
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
'''.format(
                        id=self.number,
                        user=str(self.user) if getattr(self, "user", None) else '(Not assigned yet)',
                        title=self.title,
                        description=self.description,
                        sign=settings.SITE_HEADER,
                    ),
                    settings.APP_EMAIL,
                    emails_to,
                )
            except Exception as e:
                logger.warning("[Task #%s] Error trying to send the task creation email - %s: %s",
                               self.number, e.__class__.__name__, str(e))


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Check List")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(_("description"), max_length=200)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return self.item_description
