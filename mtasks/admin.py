from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Task, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('id', 'title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fieldsets = (               # Edition form
        (None,               {'fields': ('title', ('description', 'resolution'))}),
        ('Date information', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    inlines = [ItemInline]
    readonly_fields = ('created_at',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 4,
                                  'cols': 32})},
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(TaskAdmin, self).get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('title', 'description')}),
            )
        return fieldsets


admin.site.register(Task, TaskAdmin)
