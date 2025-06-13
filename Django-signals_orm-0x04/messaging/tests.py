from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message_send(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        self.assertTrue(Notification.objects.filter(user=self.receiver, message=message).exists())

    def test_message_history_logged_on_edit(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Original')
        message.content = 'Edited'
        message.save()
        self.assertTrue(MessageHistory.objects.filter(message=message).exists())

    def test_user_deletion_cleans_up_data(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Bye')
        Notification.objects.create(user=self.receiver, message=message)
        self.sender.delete()
        self.assertFalse(Message.objects.exists())
        self.assertFalse(Notification.objects.exists())