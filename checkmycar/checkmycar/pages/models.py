from django.db import models


class QuoteRequest(models.Model):
    publication_id = models.CharField(max_length=10, blank=True)
    publication_title = models.CharField(max_length=50, blank=True)
    vehicle_brand = models.CharField(max_length=20, blank=True)
    vehicle_model = models.CharField(max_length=20, blank=True)
    vehicle_kilometers = models.CharField(max_length=30, blank=True)
    seller_address_city = models.CharField(max_length=20, blank=True)
    seller_address_state = models.CharField(max_length=20, blank=20)
    seller_address_country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.publication_id} - {self.vehicle_brand}, {self.vehicle_model} | {self.seller_address_city}"

     
class MechanicalWorkshop(models.Model):
    commercial_name = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    is_official_workshop = models.BooleanField(default=False)
    brands_specialities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.commercial_name} | {self.city}"

class Mechanic(models.Model):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    mechanical_workshop = models.ForeignKey(MechanicalWorkshop, null=True, related_name='mechanics', on_delete=models.DO_NOTHING)
    #independent = models.BooleanField(default=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    specialities = models.TextField(blank=True)
    default_available_days = models.TextField(blank=True)
    default_available_hours = models.TextField(blank=True)
    checking_plans = models.ManyToManyField('CheckingPlan', related_name='checking_plans')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.mechanical_workshop.commercial_name} | {self.city}"


class CheckingPlan(models.Model):
    title = models.CharField(max_length=30)
    cost = models.FloatField()

    def __str__(self):
        return f"{self.title} {self.cost}"

class Service(models.Model):
    title = models.CharField(max_length=20)
    special_tool_required = models.BooleanField(default=False)
    special_tools = models.CharField(max_length=50, blank=True)
    requires_workshop = models.BooleanField(default=False)
    hours_required = models.FloatField()
    checking_plan = models.ForeignKey(CheckingPlan, related_name='services', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.title}"
