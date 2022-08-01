from django.contrib import admin

from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake,CarModelAdmin)
admin.site.register(CarModel)