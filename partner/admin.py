from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phones', 'address', 'is_company')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'email')

    ordering = ('name',)
    list_filter = ('is_company',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
    fieldsets = (  # Edition form
        (None, {'fields': (('name', 'is_company'), ('email', 'website'), ('phone', 'mobile'), ('address',), ('comment',))}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': (('name', 'is_company'), ('email', 'website'), ('phone', 'mobile'), ('address',), ('comment',))}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Partner, PartnerAdmin)
