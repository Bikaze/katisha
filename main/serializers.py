from rest_framework import serializers
from .models import Passenger, Route, Ticket, TicketTemplate, Vehicle


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


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    ticket_template = TicketTemplateSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'passenger', 'ticket_template', 'payment_status', 'purchase_date', 'created_at']


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['passenger', 'payment_status']


    def create(self, validated_data):
        ticket_template_id = self.context.get('ticket_template_id') # noqa
        return Ticket.objects.create(ticket_template_id=ticket_template_id, **validated_data)


class PassengerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    wallet_balance = serializers.SerializerMethodField(method_name='get_wallet_balance', read_only=True)

    class Meta:
        model = Passenger
        fields = ['id', 'birthdate', 'phone', 'wallet_balance']

    def get_wallet_balance(self, obj: Passenger):
        return obj.wallet.balance


class UpdatePassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['birthdate', 'phone']
