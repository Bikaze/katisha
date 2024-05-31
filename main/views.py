from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
from .models import Ticket, TicketTemplate, Vehicle
from .serializers import AddTicketTemplateSerializer, CreateTicketSerializer, TicketSerializer, TicketTemplateSerializer, VehicleSerializer

class TicketTemplateViewSet(viewsets.ModelViewSet):
    queryset = TicketTemplate.objects.select_related('route', 'vehicle__company').all()
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketTemplateSerializer
        return AddTicketTemplateSerializer
    # permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return TicketTemplate.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.select_related('company').all()
    serializer_class = VehicleSerializer


# class PassengerViewSet(viewsets.ModelViewSet):
#     queryset = Passenger.objects.select_related('user').all()
#     serializer_class = PassengerSerializer


class TicketViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Ticket.objects.select_related('ticket_template__route',
                                             'ticket_template__vehicle__company',
                                             'passenger__user',
                                             ).filter(
                                                ticket_template_id=self.kwargs.get('ticket_pk')
                                             )
    

    def get_serializer_context(self):
        return {'ticket_template_id': self.kwargs.get('ticket_pk')}
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketSerializer
        return CreateTicketSerializer
