# Generated by Django 4.1.4 on 2023-01-08 21:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CheckingPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("summary", models.TextField(blank=True)),
                ("cost", models.FloatField()),
                ("logo", models.ImageField(blank=True, null=True, upload_to="logos/")),
            ],
        ),
        migrations.CreateModel(
            name="MechanicalWorkshop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("commercial_name", models.CharField(blank=True, max_length=50)),
                ("city", models.CharField(blank=True, max_length=20)),
                ("state", models.CharField(blank=True, max_length=20)),
                ("country", models.CharField(blank=True, max_length=20)),
                ("brief_description", models.TextField(blank=True)),
                ("is_official_workshop", models.BooleanField(default=False)),
                ("brands_specialities", models.TextField(blank=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="logos/")),
                (
                    "distance_availability",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="Distance dispuesto a realizar para revisar un vehiculo (en Kms)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuoteRequest",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("publication_id", models.CharField(blank=True, max_length=10)),
                ("publication_title", models.CharField(blank=True, max_length=50)),
                ("vehicle_brand", models.CharField(blank=True, max_length=20)),
                ("vehicle_model", models.CharField(blank=True, max_length=20)),
                ("vehicle_kilometers", models.CharField(blank=True, max_length=30)),
                ("seller_address_city", models.CharField(blank=True, max_length=20)),
                ("seller_address_state", models.CharField(blank=20, max_length=20)),
                ("seller_address_country", models.CharField(blank=True, max_length=20)),
                ("phone_number", models.IntegerField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=40)),
                ("special_tool_required", models.BooleanField(default=False)),
                ("special_tools", models.CharField(blank=True, max_length=50)),
                ("requires_workshop", models.BooleanField(default=False)),
                ("hours_required", models.FloatField()),
                (
                    "checking_plan",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="services",
                        to="pages.checkingplan",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Mechanic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=20)),
                ("last_name", models.CharField(blank=True, max_length=20)),
                ("brief_description", models.TextField(blank=True)),
                ("independent", models.BooleanField(default=True)),
                ("approved", models.BooleanField(default=False)),
                ("city", models.CharField(blank=True, max_length=20)),
                ("state", models.CharField(blank=True, max_length=20)),
                ("country", models.CharField(blank=True, max_length=20)),
                ("specialities", models.TextField(blank=True)),
                ("available_during_morning", models.BooleanField(default=True)),
                ("avaialble_during_afternoon", models.BooleanField(default=True)),
                (
                    "years_of_experience",
                    models.PositiveIntegerField(blank=True, default=0),
                ),
                (
                    "checking_plans",
                    models.ManyToManyField(
                        related_name="mechanics", to="pages.checkingplan"
                    ),
                ),
                (
                    "mechanical_workshop",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="mechanics",
                        to="pages.mechanicalworkshop",
                    ),
                ),
            ],
        ),
    ]
