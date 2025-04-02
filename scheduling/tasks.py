from celery import shared_task
from .models import Flight

@shared_task
def auto_update_flight_status():
    flights = Flight.objects.all()
    for flight in flights:
        flight.update_status()
