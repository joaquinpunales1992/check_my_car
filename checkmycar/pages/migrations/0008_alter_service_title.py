# Generated by Django 4.1.4 on 2022-12-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0007_mechanicalworkshop_brief_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service", name="title", field=models.CharField(max_length=40),
        ),
    ]