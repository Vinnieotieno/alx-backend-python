rom django.views.decorators.cache import cache_page
from django.shortcuts import render
from messaging.models import Message

@cache_page(60)
def cached_conversation_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').prefetch_related('replies')
    return render(request, 'conversation.html', {'messages': messages})