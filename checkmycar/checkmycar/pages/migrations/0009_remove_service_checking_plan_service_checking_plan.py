# Generated by Django 4.1.4 on 2022-12-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0008_alter_service_title"),
    ]

    operations = [
        migrations.RemoveField(model_name="service", name="checking_plan",),
        migrations.AddField(
            model_name="service",
            name="checking_plan",
            field=models.ManyToManyField(
                related_name="services", to="pages.checkingplan"
            ),
        ),
    ]
