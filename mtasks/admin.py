from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Task, Item
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class TaskAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'deadline', 'priority', 'state')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'item__item_description',
                     'user__username', 'user__first_name', 'user__last_name')
    list_filter = (
        ('user', RelatedDropdownFilter),
        'state',
        'priority',
        'deadline'
    )
    advanced_filter_fields = (
        'user__username',
        'state',
        'priority',
        'deadline',
        'created_at',
        'created_by',
        'title',
        'description',
        'resolution',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
    autocomplete_fields = ['user']

    fieldsets = (               # Edition form
        (None,                   {'fields': ('title', ('user', 'deadline'), ('state', 'priority'), ('description', 'resolution'))}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
    inlines = [ItemInline]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('title', ('user', 'deadline'), ('state', 'priority'), 'description')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
