# Generated by Django 4.1.4 on 2022-12-28 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_mechanic_quoterequest_seller_address_city_and_more"),
    ]

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
                ("cost", models.FloatField()),
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
                ("is_official_workshop", models.BooleanField(default=False)),
                ("brands_specialities", models.TextField(blank=True)),
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
                ("title", models.CharField(max_length=20)),
                ("special_tool_required", models.BooleanField(default=False)),
                ("special_tools", models.CharField(blank=True, max_length=50)),
                ("requires_workshop", models.BooleanField(default=False)),
                ("hours_required", models.FloatField()),
                (
                    "checking_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="services",
                        to="pages.checkingplan",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="mechanic",
            name="checking_plans",
            field=models.ManyToManyField(
                related_name="checking_plans", to="pages.checkingplan"
            ),
        ),
        migrations.AddField(
            model_name="mechanic",
            name="mechanical_workshop",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="mechanics",
                to="pages.mechanicalworkshop",
            ),
        ),
    ]
