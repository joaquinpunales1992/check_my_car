from django.contrib import admin
from pages.models import QuoteRequest, Mechanic, MechanicalWorkshop, Service, CheckingPlan
 

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'mechanical_workshop', 'city',]

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuoteRequest._meta.get_fields()]

@admin.register(MechanicalWorkshop)
class MechanicalWorkshopAdmin(admin.ModelAdmin):
    list_display = ['commercial_name', 'city', 'is_official_workshop',]
    #list_display = [field.name for field in MechanicalWorkshop._meta.get_fields()]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.get_fields()]

@admin.register(CheckingPlan)
class CheckingPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'cost',]
