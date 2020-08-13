from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from task_manager.models import Task


@receiver(post_save, sender=Task)
def my_handler(sender, instance, created, **kwargs):
    user = User.objects.filter(is_superuser=True)
    notify.send(instance, recipient=user, verb='was saved')


# post_save.connect(my_handler, sender=Task)