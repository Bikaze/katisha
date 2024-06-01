from django_filters.rest_framework import FilterSet
from .models import TicketTemplate


class TicketTemplateFilter(FilterSet):
    class Meta:
        model = TicketTemplate
        fields = {
            'departure_date': ['exact'],
            'departure_time': ['gt', 'lt'],
        }
        