from django.urls import path, include
from rest_framework_nested import routers
from .views import PassengerViewSet, TicketHistoryViewSet, TicketTemplateViewSet, GeneratedTicketViewSet, WalletViewSet

router = routers.DefaultRouter()
router.register('tickets', TicketTemplateViewSet)
router.register('users', PassengerViewSet)

created_ticket_router = routers.NestedDefaultRouter(router, 'tickets', lookup='ticket')
created_ticket_router.register('created-tickets', GeneratedTicketViewSet, basename='ticket-tickets')
wallet_history_ticket_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
wallet_history_ticket_router.register('ticket-history', TicketHistoryViewSet, basename='ticket_history')
wallet_history_ticket_router.register('wallet', WalletViewSet, basename='top-up')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(created_ticket_router.urls)),
    path('', include(wallet_history_ticket_router.urls)),
]

