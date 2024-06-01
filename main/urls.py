from django.urls import path, include
from rest_framework_nested import routers
from .views import PassengerViewSet, TicketHistoryViewSet, TicketTemplateViewSet, GeneratedTicketViewSet

router = routers.DefaultRouter()
router.register('tickets', TicketTemplateViewSet)
router.register('users', PassengerViewSet)

created_ticket_router = routers.NestedDefaultRouter(router, 'tickets', lookup='ticket')
created_ticket_router.register('created-tickets', GeneratedTicketViewSet, basename='ticket-tickets')
history_ticket_router = routers.NestedDefaultRouter(router, 'users', lookup='user_tickets')
history_ticket_router.register('ticket-history', TicketHistoryViewSet, basename='ticket_history')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(created_ticket_router.urls)),
    path('', include(history_ticket_router.urls)),
]

