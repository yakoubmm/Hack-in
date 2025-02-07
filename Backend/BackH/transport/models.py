from django.db import models

from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # New field: allows each station to be linked with multiple (or zero) Transport objects.
    available_transports = models.ManyToManyField('Transport', blank=True, related_name="stations")

    def __str__(self):
        return self.name



class Transport(models.Model):
    TAXI = 'taxi'
    BUS = 'Kous'
    TRAM = 'tram'
    TRAIN = 'train'
    METRO = 'metro'
    TRANSPORT_CHOICES = [
        (TAXI, 'Taxi'),
        (BUS, 'Kous'),
        (TRAM, 'Tramway'),
        (TRAIN, 'Train'),
        (METRO, 'Metro'),
    ]
    type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.PositiveIntegerField(help_text="Time in minutes for this segment")

    def __str__(self):
        return f"{self.get_type_display()} (Cost: {self.cost}, Time: {self.time} min)"


class Journey(models.Model):
    start_station = models.ForeignKey(
        Station, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="journeys_started"
    )
    end_station = models.ForeignKey(
        Station, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="journeys_ended"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Journey from {self.start_station} to {self.end_station}"

    def total_duration(self):
        segments = self.route_segments.all().order_by('segment_order')
        return sum(segment.transport.time for segment in segments)

    def total_cost(self):
        segments = self.route_segments.all().order_by('segment_order')
        return sum(segment.transport.cost for segment in segments)

    def total_distance(self):
        segments = self.route_segments.all().order_by('segment_order')
        # Assuming each segment has a 'distance' (which may be optional)
        return sum(segment.distance for segment in segments if segment.distance is not None)


class RouteSegment(models.Model):
    journey = models.ForeignKey(
        Journey, 
        on_delete=models.CASCADE, 
        related_name='route_segments'
    )
    source_station = models.ForeignKey(
        Station, 
        on_delete=models.CASCADE, 
        related_name='route_segments_from'
    )
    destination_station = models.ForeignKey(
        Station, 
        on_delete=models.CASCADE, 
        related_name='route_segments_to'
    )
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    segment_order = models.PositiveIntegerField(help_text="The order of this segment within the journey")
    distance = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Distance in kilometers (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['segment_order']

    def __str__(self):
        return (f"Segment {self.segment_order}: {self.source_station} "
                f"to {self.destination_station} via {self.transport}")
