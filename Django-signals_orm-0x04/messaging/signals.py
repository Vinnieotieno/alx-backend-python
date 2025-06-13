from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is None:
        return
    try:
        old = Message.objects.get(pk=instance.pk)
        if old.content != instance.content:
            MessageHistory.objects.create(message=old, old_content=old.content)
            instance.edited = True
    except Message.DoesNotExist:
        pass