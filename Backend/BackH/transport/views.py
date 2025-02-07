from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Journey
from .serializers import JourneySerializer

@api_view(['GET'])
def journey_list(request):
    """
    Retrieve a list of journeys.
    Optionally filter by source and destination using query parameters.
    For example:
        /api/journeys/?source=Station A&destination=Station B
    """
    # Start with all journeys
    journeys = Journey.objects.all()
    
    # Optional filtering based on query parameters
    source = request.query_params.get('source')
    destination = request.query_params.get('destination')
    
    if source and destination:
        journeys = journeys.filter(
            start_station__name=source,
            end_station__name=destination
        )
    
    serializer = JourneySerializer(journeys, many=True)
    return Response(serializer.data)
