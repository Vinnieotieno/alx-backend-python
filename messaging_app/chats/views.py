from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        participant_ids = request.data.get('participants', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response({'error': 'A conversation requires at least 2 participants.'},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-sent_at']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
