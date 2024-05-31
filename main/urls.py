from django.urls import path, include
from rest_framework_nested import routers
from .views import PassengerViewSet, TicketTemplateViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register('tickets', TicketTemplateViewSet)
router.register('users', PassengerViewSet)

created_ticket_router = routers.NestedDefaultRouter(router, 'tickets', lookup='ticket')
created_ticket_router.register('created-tickets', TicketViewSet, basename='ticket-tickets')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(created_ticket_router.urls)),
]

