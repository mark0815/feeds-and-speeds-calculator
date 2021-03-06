from django.contrib import admin
from feeds_and_speeds.models import Machine, MaterialClass, Material, Tool, CuttingSpeeds, ToolVendor, CuttingRecipe

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "spindle_power", "max_rpm",
                    "max_cutting_speed", "active")


@admin.register(MaterialClass)
class MaterialClassAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("material_class", "name", "kc_1_1", "mc")


@admin.register(ToolVendor)
class ToolVendorAdmin(admin.ModelAdmin):
    list_display = ("name", "tool_count")

    def tool_count(self, obj: ToolVendor):
        return obj.tools.count()


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("vendor", "name", "flute_count", "diameter",
                    "flute_length", "fz_factor_at_one_ae", "vc_factor_at_one_ae")
    list_filter = ("vendor",)


@admin.register(CuttingSpeeds)
class CuttingSpeedsAdmin(admin.ModelAdmin):
    list_display = ("tool", "material", "feed_per_tooth", "cutting_speed")


@admin.register(CuttingRecipe)
class CuttingRecipeAdmin(admin.ModelAdmin):
    list_display = ("cutter_data", "ae", "ap",
                    "calculated_rpm", "calculated_feed")
    list_filter = ("cutter_data__material", "cutter_data__tool")

    def calculated_rpm(self, obj: CuttingRecipe):
        machine = Machine.objects.filter(active=True).first()
        return "%.0f" % obj.feeds_and_speeds(machine=machine)[0]

    calculated_rpm.short_description = 'Calculated RPM (1/min)'

    def calculated_feed(self, obj: CuttingRecipe):
        machine = Machine.objects.filter(active=True).first()
        return "%.0f" % obj.feeds_and_speeds(machine=machine)[1]

    calculated_feed.short_description = 'Calculated Feed (mm/min)'
