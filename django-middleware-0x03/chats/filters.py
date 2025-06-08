import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='gte')
    end = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='lte')
    participant = django_filters.NumberFilter(field_name="conversation__participants__id")

    class Meta:
        model = Message
        fields = ['participant', 'start', 'end']
