from rest_framework import serializers
from .models import Route, TicketTemplate, Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        fields = ['plate_number', 'capacity', 'company']


# class RouteSerializer(serializers.Serializer):
#     class Meta:
#         model = Route
#         fields = ['origin', 'destination']
    


class TicketTemplateSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    route = serializers.StringRelatedField()

    class Meta:
        model = TicketTemplate
        fields = ['id', 'route', 'vehicle', 'price', 'departure_date', 'departure_time', 'inventory']


class AddTicketTemplateSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField()
    route_id = serializers.IntegerField()

    def validate_vehicle_id(self, value):
        if not Vehicle.objects.filter(id=value).exists():
            raise serializers.ValidationError('Vehicle does not exist')
        return value
    
    def validate_route_id(self, value):
        if not Route.objects.filter(id=value).exists():
            raise serializers.ValidationError('Route does not exist')
        return value
    
    def validate_inventory(self, value):
        vehicle_id = self.initial_data.get('vehicle_id')
        if vehicle_id:
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()
            if vehicle and value > vehicle.capacity:
                raise serializers.ValidationError('Inventory must be less than or equal to vehicle capacity')
        return value
    
    class Meta:
        model = TicketTemplate
        fields = ['route_id', 'vehicle_id', 'price', 'departure_date', 'departure_time', 'inventory']
