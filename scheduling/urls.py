from django.urls import path
from . import views

from django.http import JsonResponse

"""def flight_status(request):
    return JsonResponse({"status": "Feature not implemented yet"}, status=501)"""
urlpatterns = [
    path('', views.home, name='home'),
    path('flights/', views.flight_list, name='flight_list'),
    path('cargo/', views.cargo_list, name='cargo_list'),
    path('schedule-flight/', views.schedule_flight, name='schedule_flight'),
    path('schedule-cargo/', views.schedule_cargo, name='schedule_cargo'),
    path('api/flight-chart-data/', views.flight_chart_data, name='flight_chart_data'),
    path('api/ai-flight-recommendations/', views.ai_flight_recommendations, name='ai_flight_recommendations'),
    path('api/ai-cargo-allocation/', views.ai_cargo_allocation, name='ai_cargo_allocation'),
    # path("api/flight-status/", flight_status, name="flight_status"),
    path("api/update-flight-status/<int:flight_id>/", views.ai_update_flight_status, name="update_flight_status"),
    path("api/flight-status/", views.flight_status, name="flight_status"),
    path('api/update-flight-status/<int:flight_id>/', views.update_flight_status, name='update_flight_status'),
    path("add-cargo/", views.add_cargo, name="add_cargo"),

]
