# Generated by Django 5.1.7 on 2025-04-02 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduling", "0007_flight_original_arrival_time_alter_flight_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="cargo",
            name="priority",
            field=models.CharField(
                choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
                default="Medium",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="base_cost_per_km",
            field=models.FloatField(default=3.0, help_text="Base cost per km in INR"),
        ),
    ]
