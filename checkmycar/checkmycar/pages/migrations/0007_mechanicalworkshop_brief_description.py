# Generated by Django 4.1.4 on 2022-12-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0006_mechanic_brief_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="mechanicalworkshop",
            name="brief_description",
            field=models.TextField(blank=True),
        ),
    ]
