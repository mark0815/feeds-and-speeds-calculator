from django.contrib import admin
from feeds_and_speeds.models import Machine, MaterialClass, Material, Tool, CuttingSpeeds, ToolVendor

# Register your models here.


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "spindle_power", "max_rpm", "max_cutting_speed")


@admin.register(MaterialClass)
class MaterialClassAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("material_class", "name", "kc_1_1", "mc")

    

@admin.register(ToolVendor)
class ToolVendorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("vendor", "name", "flute_count", "diameter")


@admin.register(CuttingSpeeds)
class CuttingSpeedsAdmin(admin.ModelAdmin):
    list_display = ("material", "tool", "feed_per_tooth", "cutting_speed")
