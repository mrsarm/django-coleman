from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, null=True, blank=True)
    resolution = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.id, self.description)


class Item(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.item_description
