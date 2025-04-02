from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
import datetime

class Flight(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Delayed', 'Delayed'),
        ('On Time', 'On Time'),
        ('Taken Off', 'Taken Off'),
        ('Landed', 'Landed'),
        ('Cancelled', 'Cancelled'),
    ]

    flight_number = models.CharField(max_length=10, unique=True)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    # original_arrival_time = models.DateTimeField(null=True, blank=True)
    available_seats = models.IntegerField()
    cargo_capacity = models.FloatField(help_text='Capacity in tons')
    base_cost_per_km = models.FloatField(default=3.0, help_text="Base cost per km in INR")  # New field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled'
    )

    def __str__(self):
        return f"{self.flight_number} ({self.departure_city} -> {self.arrival_city})"

    def update_status(self):
        """
        AI-based status update based on time
        """
        current_time = datetime.datetime.now()

        if self.status in ["Landed", "Cancelled"]:
            return  # Do not update if already landed or cancelled

        if current_time >= self.departure_time and current_time < self.arrival_time:
            self.status = "Taken Off"
        elif current_time >= self.arrival_time:
            self.status = "Landed"
        elif self.departure_time - datetime.timedelta(minutes=30) <= current_time < self.departure_time:
            self.status = "On Time"
        elif current_time < self.departure_time - datetime.timedelta(hours=1):
            self.status = "Scheduled"
        else:
            self.status = "Delayed"

        self.save()


class Cargo(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    cargo_id = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    weight = models.FloatField(validators=[MinValueValidator(0.1)])
    departure_city = models.CharField(max_length=100, default="Unknown")
    destination = models.CharField(max_length=100, default="Unknown", db_index=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")  # New field
    allocated = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cargo_id} - {self.departure_city} → {self.destination} ({self.priority})"

    def get_status(self):
        return "Allocated" if self.allocated else "Pending"
