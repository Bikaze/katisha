from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Passenger, Route, Ticket, TicketTemplate, Vehicle, Wallet


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
    passenger = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = ['id', 'passenger', 'ticket_template', 'created_at']


class CreateTicketSerializer(serializers.ModelSerializer):
    passenger = serializers.StringRelatedField(read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'passenger']


    def create(self, validated_data):
        user_id = self.context.get('request').user.id
        passenger = get_object_or_404(Passenger, user_id=user_id)
        ticket_template_id = self.context.get('ticket_template_id') # noqa
        ticket_template = get_object_or_404(TicketTemplate, pk=ticket_template_id)

        if passenger.wallet.balance < ticket_template.price:
            raise serializers.ValidationError('Insufficient funds')
        
        passenger.wallet.balance -= ticket_template.price
        passenger.wallet.save()

        ticket_template.inventory -= 1
        ticket_template.save()

        return Ticket.objects.create(ticket_template=ticket_template, passenger=passenger)


class PassengerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    wallet_balance = serializers.SerializerMethodField(method_name='get_wallet_balance', read_only=True)
    username = serializers.StringRelatedField(source='user.username', read_only=True)
    first_name = serializers.StringRelatedField(source='user.first_name', read_only=True)
    last_name = serializers.StringRelatedField(source='user.last_name', read_only=True)

    class Meta:
        model = Passenger
        fields = ['id', 'username', 'first_name', 'last_name', 'birthdate', 'phone', 'wallet_balance']

    def get_wallet_balance(self, obj: Passenger):
        return obj.wallet.balance


class UpdatePassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['birthdate', 'phone']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance']

