from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=255)
    spindle_power = models.FloatField(verbose_name="Spindle net power (kW)")
    max_rpm = models.PositiveIntegerField(
        verbose_name="Max spindle RPM (1/min)")
    max_cutting_speed = models.PositiveIntegerField(
        verbose_name="max cutting speed (mm/min)")

    def __str__(self):
        return "%s" % self.name


class MaterialClass(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Material(models.Model):
    material_class = models.ForeignKey(
        MaterialClass,
        on_delete=models.CASCADE,
        related_name="materials"
    )
    name = models.CharField(max_length=255)
    kc_1_1 = models.FloatField(verbose_name="kc 1.1 (N/mm^2)")
    mc = models.FloatField(verbose_name="Mc")

    def __str__(self):
        return "%s (%s)" % (self.name, self.material_class)


class ToolVendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Tool(models.Model):
    vendor = models.ForeignKey(
        ToolVendor,
        on_delete=models.CASCADE,
        related_name="tools",
        null=True
    )
    name = models.CharField(max_length=255)
    flute_count = models.PositiveIntegerField(verbose_name="Flute count")
    diameter = models.FloatField(verbose_name="Diameter (mm)")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.name



class CuttingSpeeds(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    feed_per_tooth = models.FloatField(
        verbose_name="Feed per Tooth (mm)")
    cutting_speed = models.FloatField(
        verbose_name="Cutting Speed (m/min)")
