# chats/views.py
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from messaging.models import Message

@cache_page(60)
def conversation_view(request, user_id):
    messages = Message.objects.filter(receiver_id=user_id).select_related('sender').prefetch_related('replies')
    return render(request, 'conversation.html', {'messages': messages})