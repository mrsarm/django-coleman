from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


phones_tr = _("phones")


class Partner(models.Model):
    """
    A Partner can be a customer, a provider, a contact, you should
    extend this model to add business logic related with your
    partners' relationship
    """
    class Meta:
        ordering = ["name"]
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    name = models.CharField(_("name"), max_length=200)
    email = models.EmailField(_("email"))
    website = models.URLField(_("website"), blank=True)
    is_company = models.BooleanField(_("is a company"), default=False)
    phone = models.CharField(_("phone"), max_length=40, null=True, blank=True)
    mobile = models.CharField(_("mobile"), max_length=40, null=True, blank=True)
    address = models.CharField(_("address"), max_length=128, null=True, blank=True)
    comment = models.TextField(_("notes"), max_length=2000, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def phones(self):
        return ", ".join(filter(None, (self.phone, self.mobile)))
