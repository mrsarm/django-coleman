from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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
        ('20_critical', _('Critical')),
        ('30_blocker', _('Blocker'))
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.id, self.title)


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Check List")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(_("description"), max_length=200)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return self.item_description
