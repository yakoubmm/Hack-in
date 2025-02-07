from rest_framework import serializers
from .models import Station, Transport, Journey, RouteSegment

class StationSerializer(serializers.ModelSerializer):
    # Show the available transports using their string representation.
    available_transports = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Station
        fields = ['id', 'name', 'location', 'available_transports']


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id', 'type', 'cost', 'time']


class RouteSegmentSerializer(serializers.ModelSerializer):
    # Nest serializers to provide details for the source, destination, and transport.
    source_station = StationSerializer(read_only=True)
    destination_station = StationSerializer(read_only=True)
    transport = TransportSerializer(read_only=True)
    
    class Meta:
        model = RouteSegment
        fields = ['id', 'segment_order', 'source_station', 'destination_station', 'transport', 'distance', 'created_at', 'updated_at']


class JourneySerializer(serializers.ModelSerializer):
    # Nest serializers for the start and end stations and all route segments.
    start_station = StationSerializer(read_only=True)
    end_station = StationSerializer(read_only=True)
    route_segments = RouteSegmentSerializer(many=True, read_only=True)
    
    # Include aggregated values as read-only fields.
    total_duration = serializers.FloatField(read_only=True, source='total_duration')
    total_cost = serializers.FloatField(read_only=True, source='total_cost')
    total_distance = serializers.FloatField(read_only=True, source='total_distance')
    
    class Meta:
        model = Journey
        fields = [
            'id',
            'start_station',
            'end_station',
            'notes',
            'created_at',
            'updated_at',
            'route_segments',
            'total_duration',
            'total_cost',
            'total_distance',
        ]
