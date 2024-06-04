from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .filters import TicketTemplateFilter
# from rest_framework.permissions import AllowAny
from .models import Passenger, Ticket, TicketTemplate, Vehicle, Wallet
from .serializers import (    
                            AddTicketTemplateSerializer,
                            CreateTicketSerializer,
                            PassengerSerializer,
                            TicketSerializer,
                            TicketTemplateSerializer,
                            UpdatePassengerSerializer,
                            VehicleSerializer,
                            WalletSerializer,
                        )

from rest_framework.decorators import action
from rest_framework.response import Response

class TicketTemplateViewSet(viewsets.ModelViewSet):
    queryset = TicketTemplate.objects.select_related('route', 'vehicle__company').all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['route__destination', 'vehicle__company__name']
    filterset_class = TicketTemplateFilter
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketTemplateSerializer
        return AddTicketTemplateSerializer
    # permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.select_related('company').all()
    serializer_class = VehicleSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.select_related('user', 'wallet').all()
    serializer_class = PassengerSerializer
    http_method_names = ['get', 'head', 'options', 'patch', 'delete']

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        passenger = Passenger.objects.select_related('user', 'wallet').get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = PassengerSerializer(passenger)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UpdatePassengerSerializer(passenger, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdatePassengerSerializer
        return PassengerSerializer


class GeneratedTicketViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Ticket.objects.select_related('ticket_template__route',
                                             'ticket_template__vehicle__company',
                                             'passenger__user',
                                             ).filter(
                                                ticket_template_id=self.kwargs.get('ticket_pk')
                                             )
    

    def get_serializer_context(self):
        return {'ticket_template_id': self.kwargs.get('ticket_pk'),
                'request': self.request
                }
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketSerializer
        return CreateTicketSerializer
    

class TicketHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Ticket.objects.select_related('ticket_template__route',
                                             'ticket_template__vehicle__company',
                                             'passenger__user',
                                             ).filter(
                                                passenger__user_id=user_id
                                             )

    
class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    http_method_names = ['get', 'head', 'options', 'patch']

    def get_queryset(self):
        user_id = self.request.user.id
        # passenger = Passenger.objects.get(user_id=user_id)
        return Wallet.objects.select_related('passenger__user').filter(passenger__user_id=user_id)
