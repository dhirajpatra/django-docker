from django.contrib import admin
from django.contrib.admin import AdminSite

from task_manager import models
# Register your models here.
# admin.site.register(models.Task)
admin.site.register(models.Comment)


class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        request.user.notifications.mark_all_as_read()
        return super(MyModelAdmin, self).get_queryset(request)


admin.site.register(models.Task, MyModelAdmin)