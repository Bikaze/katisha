from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
from .models import TicketTemplate, Vehicle
from .serializers import AddTicketTemplateSerializer, TicketTemplateSerializer, VehicleSerializer

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