from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Flight, Cargo
import random, heapq, logging,json, pytz
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, is_naive, now
from .forms import CargoForm


# Create your views here.
# Indian city graph with estimated distances (in km)
INDIAN_CITY_GRAPH = {
    "Mumbai": {"Delhi": 1400, "Bengaluru": 980, "Chennai": 1330, "Pune": 150, "Ahmedabad": 520},
    "Delhi": {"Mumbai": 1400, "Kolkata": 1500, "Hyderabad": 1260, "Jaipur": 270},
    "Bengaluru": {"Mumbai": 980, "Chennai": 350, "Hyderabad": 570, "Kochi": 540},
    "Chennai": {"Mumbai": 1330, "Bengaluru": 350, "Kolkata": 1650, "Visakhapatnam": 800},
    "Kolkata": {"Delhi": 1500, "Chennai": 1650, "Hyderabad": 1200, "Bhubaneswar": 440},
    "Hyderabad": {"Delhi": 1260, "Bengaluru": 570, "Kolkata": 1200, "Visakhapatnam": 600},
    "Pune": {"Mumbai": 150, "Hyderabad": 560, "Ahmedabad": 660},
    "Ahmedabad": {"Mumbai": 520, "Jaipur": 670, "Delhi": 930},
    "Jaipur": {"Delhi": 270, "Ahmedabad": 670},
    "Kochi": {"Bengaluru": 540, "Chennai": 690},
    "Visakhapatnam": {"Chennai": 800, "Hyderabad": 600, "Bhubaneswar": 450},
    "Bhubaneswar": {"Kolkata": 440, "Visakhapatnam": 450}
}
logger = logging.getLogger(__name__)

# A* Search Algorithm for finding the lowest-cost path
def a_star_search(start, goal):
    if start not in INDIAN_CITY_GRAPH or goal not in INDIAN_CITY_GRAPH:
        return None, float('inf')

    queue = [(0, start, [])]  # (cost, city, path)
    visited = set()

    while queue:
        cost, city, path = heapq.heappop(queue)

        if city in visited:
            continue
        visited.add(city)
        path = path + [city]

        if city == goal:
            return path, cost

        for neighbor, distance in INDIAN_CITY_GRAPH[city].items():
            if neighbor not in visited:
                estimated_cost = cost + distance
                heapq.heappush(queue, (estimated_cost, neighbor, path))

    return None, float('inf')


# Simulated AI model for flight scheduling recommendations
# AI-based Flight Recommendations
def ai_flight_recommendations(request):
    departure_city = request.GET.get("departure_city")
    arrival_city = request.GET.get("arrival_city")

    if not departure_city or not arrival_city:
        return JsonResponse({"error": "Please enter both departure and arrival cities"}, status=400)

    if departure_city not in INDIAN_CITY_GRAPH or arrival_city not in INDIAN_CITY_GRAPH:
        return JsonResponse({"error": "No valid route found"}, status=404)

    path, distance = a_star_search(departure_city, arrival_city)

    if path is None:
        return JsonResponse({"error": "No valid route found"}, status=404)

    best_departure_time = datetime.now() + timedelta(hours=random.randint(2, 6))
    best_arrival_time = best_departure_time + timedelta(hours=(distance // 500) + 1)
    suggested_price = 3 * distance  # ₹3 per km
    available_seats = random.randint(50, 200)
    cargo_capacity = random.uniform(5, 20)

    return JsonResponse({
        "path": path,
        "best_departure_time": best_departure_time.strftime("%Y-%m-%d %H:%M"),
        "best_arrival_time": best_arrival_time.strftime("%Y-%m-%d %H:%M"),
        "suggested_price": suggested_price,
        "available_seats": available_seats,
        "cargo_capacity": round(cargo_capacity, 1)
    })


# Flight Scheduling View
def schedule_flight(request):
    if request.method == "POST":
        Flight.objects.create(
            flight_number=request.POST['flight_number'],
            departure_city=request.POST['departure_city'],
            arrival_city=request.POST['arrival_city'],
            departure_time=request.POST['departure_time'],
            arrival_time=request.POST['arrival_time'],
            available_seats=request.POST['available_seats'],
            cargo_capacity=request.POST['cargo_capacity'],
        )
        return redirect('/')
    return render(request, 'schedule_flight.html')

# AI-based Cargo Allocation Recommendations
def ai_cargo_allocation(request):
    destination = request.GET.get("destination")
    print(f"🚀 Received request for destination: {destination}")

    if not destination or destination not in INDIAN_CITY_GRAPH:
        return JsonResponse({"error": f"No AI recommendations for {destination} yet."}, status=404)

    available_flights = Flight.objects.filter(arrival_city=destination, status="Scheduled").order_by("departure_time")
    print(f"✈️ Found {available_flights.count()} flights.")

    if not available_flights.exists():
        return JsonResponse({"error": "No flights available"}, status=404)

    # Find the best flight based on cargo priority
    cargo_list = Cargo.objects.filter(destination=destination, allocated=False).order_by('-priority')

    if not cargo_list.exists():
        return JsonResponse({"error": "No cargo available for this destination"}, status=404)

    best_flight = None
    min_cost = float('inf')
    best_path = None

    for flight in available_flights:
        path, distance = a_star_search(flight.departure_city, destination)

        if path and distance < min_cost:
            min_cost = distance
            best_flight = flight
            best_path = path

    if not best_flight:
        return JsonResponse({"error": "No optimal flight found"}, status=404)

    # Calculate optimized cost based on distance and cargo priority
    cost_multiplier = {"High": 1.5, "Medium": 1.2, "Low": 1.0}
    highest_priority_cargo = cargo_list.first()  # Get the highest priority cargo
    estimated_cost = min_cost * best_flight.base_cost_per_km * cost_multiplier[highest_priority_cargo.priority]

    response_data = {
        "best_flight": best_flight.flight_number,
        "path": best_path,
        "available_cargo_capacity": best_flight.cargo_capacity,
        "best_departure_time": best_flight.departure_time.strftime("%Y-%m-%d %H:%M"),
        "best_arrival_time": best_flight.arrival_time.strftime("%Y-%m-%d %H:%M"),
        "optimized_cost": round(estimated_cost, 2),
        "priority": highest_priority_cargo.priority
    }

    logger.info(f"AI Cargo Allocation Response: {response_data}")
    return JsonResponse(response_data)

def schedule_cargo(request):
    if request.method == "POST":
        cargo_id = request.POST['cargo_id']
        description = request.POST['description']
        weight = request.POST['weight']
        destination = request.POST['destination']
        allocated = request.POST['allocated'] == "True"

        # Check if the cargo already exists
        cargo, created = Cargo.objects.get_or_create(
            cargo_id=cargo_id,
            defaults={
                "description": description,
                "weight": weight,
                "destination": destination,
                "allocated": allocated
            }
        )

        # If cargo exists, update its allocation status
        if not created:
            cargo.allocated = allocated
            cargo.save()

        return redirect('/')  # Redirect to home page after submission

    return render(request, 'schedule_cargo.html')

logger = logging.getLogger(__name__)

def ai_update_flight_status(request, flight_id):
    """
    AI-based bulk update for all flights
    """
    flights = Flight.objects.all()
    updated_flights = []

    for flight in flights:
        old_status = flight.status
        flight.update_status()
        if old_status != flight.status:
            updated_flights.append({
                "flight_number": flight.flight_number,
                "old_status": old_status,
                "new_status": flight.status
            })

    return JsonResponse({"updated_flights": updated_flights})

def flight_status(request):
    flights = Flight.objects.all().values("id", "flight_number", "departure_time", "arrival_time", "status")
    return JsonResponse(list(flights), safe=False)

def update_flight_status(request, flight_id):
    return JsonResponse({'message': f'Flight {flight_id} status updated successfully'})

def flight_chart_data(request):
    data = [
        {'city': 'New York', 'passengers': 260},
        {'city': 'Los Angeles', 'passengers': 281},
        {'city': 'Chicago', 'passengers': 318},
    ]
    return JsonResponse(data, safe=False)

def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})

def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights.html', {'flights': flights})

def cargo_list(request):
    cargo = Cargo.objects.all()
    for carg in cargo:
        print(f"📦 {carg.cargo_id} | {carg.weight}kg | {carg.destination}")
    return render(request, 'cargo.html', {'cargo': cargo})

def add_cargo(request):
    if request.method == "POST":
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("✅ Cargo successfully added.")
            return JsonResponse({"message": "Cargo added successfully"}, status=201)
        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)

    form = CargoForm()
    return render(request, "add_cargo.html", {"form": form})
