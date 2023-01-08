from django.contrib import admin
from pages.models import QuoteRequest, Mechanic, MechanicalWorkshop, Service, CheckingPlan
 

# @admin.register(Mechanic)
# class MechanicAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'mechanical_workshop', 'city',]

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuoteRequest._meta.get_fields()]

# @admin.register(MechanicalWorkshop)
# class MechanicalWorkshopAdmin(admin.ModelAdmin):
#     list_display = ['commercial_name', 'city', 'is_official_workshop',]
#     #list_display = [field.name for field in MechanicalWorkshop._meta.get_fields()]

# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ['title', 'special_tool_required', 'requires_workshop', 'hours_required',]

# @admin.register(CheckingPlan)
# class CheckingPlanAdmin(admin.ModelAdmin):
#     list_display = ['title', 'cost',]


class ServiceAdmin(admin.TabularInline):
    model = Service

class CheckingPlanAdmin(admin.ModelAdmin):
   inlines = [ServiceAdmin,]

class MechanicAdmin(admin.TabularInline):
    model = Mechanic

class MechanicalWorkshopAdmin(admin.ModelAdmin):
   inlines = [MechanicAdmin,]


admin.site.register(CheckingPlan ,CheckingPlanAdmin)
admin.site.register(MechanicalWorkshop , MechanicalWorkshopAdmin)