from django import forms
from .models import Cargo

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ["cargo_id", "description", "weight", "departure_city", "destination", "priority"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "priority": forms.Select(choices=Cargo.PRIORITY_CHOICES),
        }
