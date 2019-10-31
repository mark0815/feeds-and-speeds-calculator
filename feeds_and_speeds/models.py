from django.db import models
from math import pi


class Machine(models.Model):
    name = models.CharField(max_length=255)
    spindle_power = models.FloatField(verbose_name="Spindle net power (kW)")
    max_rpm = models.PositiveIntegerField(
        verbose_name="Max spindle RPM (1/min)")
    max_cutting_speed = models.PositiveIntegerField(
        verbose_name="max cutting speed (mm/min)")
    active = models.BooleanField(verbose_name="Active Machine", default=False)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"


class MaterialClass(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Material Class"
        verbose_name_plural = "Material Classes"


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

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"


class ToolVendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Tool Vendor"
        verbose_name_plural = "Tool Vendors"


class Tool(models.Model):
    vendor = models.ForeignKey(
        ToolVendor,
        on_delete=models.CASCADE,
        related_name="tools",
        null=True
    )
    name = models.CharField(max_length=255)
    flute_count = models.PositiveIntegerField(verbose_name="Flute count")
    flute_length = models.FloatField(verbose_name='Flute length (mm) (max ap)')
    diameter = models.FloatField(verbose_name="Diameter (mm)")
    fz_factor_at_one_ae = models.FloatField(verbose_name="Fz factor at 1 Ae", default=1.0)
    vc_factor_at_one_ae = models.FloatField(verbose_name="Vc factor at 1 Ae", default=1.0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"


class CuttingSpeeds(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    feed_per_tooth = models.FloatField(
        verbose_name="Feed per Tooth (mm)")
    cutting_speed = models.FloatField(
        verbose_name="Cutting Speed (m/min)")

    def __str__(self):
        return "%s %s %.3f %.0f" % (self.tool, self.material, self.feed_per_tooth, self.cutting_speed)

    class Meta:
        verbose_name = "Cutting Speed"
        verbose_name_plural = "Cutting Speeds"


class CuttingRecipe(models.Model):
    cutter_data = models.ForeignKey(CuttingSpeeds, on_delete=models.CASCADE)
    ae = models.FloatField(
        verbose_name="Ae (width of cut) (mm)")
    ap = models.FloatField(
        verbose_name="Ap (depth of cut) (mm)")

    def is_slotting_operation(self):
        return self.ae >= self.cutter_data.tool.diameter

    def feeds_and_speeds(self, machine:Machine=None) -> (float, float):
        """ Calculate feeds and speeds based on cutter data for the given material """
        flute_count = self.cutter_data.tool.flute_count
        feed_per_tooth = self.fz_adjusted() 
        cutting_speed = self.vc_adjusted()
        cutter_diameter = self.cutter_data.tool.diameter
        rpm_calculated = (cutting_speed * 1000) / (pi * cutter_diameter)
        feed_calculated = rpm_calculated * feed_per_tooth * flute_count
        if machine:
            rpm_max = min([rpm_calculated, machine.max_rpm])
            feed_at_rpm_max = rpm_max * feed_per_tooth * flute_count
            rpm_final = feed_at_rpm_max / (feed_per_tooth * flute_count)
            return rpm_final, feed_at_rpm_max
        else:
            return rpm_calculated, feed_calculated
    
    def fz_adjusted(self):
        """ Adjust fz by the factor stored at the tool """
        tool = self.cutter_data.tool
        ae_factor = min([1,(self.ae/tool.diameter)])
        fz_factor = 1 - ((1 - tool.fz_factor_at_one_ae) * ae_factor)
        return self.cutter_data.feed_per_tooth * fz_factor
    
    def vc_adjusted(self):
        """ Adjust vc by the factor stored at the tool """
        tool = self.cutter_data.tool
        ae_factor = min([1,(self.ae/tool.diameter)])
        vc_factor = 1 - ((1 - tool.vc_factor_at_one_ae) * ae_factor)
        return self.cutter_data.cutting_speed * vc_factor

    class Meta:
        verbose_name = "Cutting Recipe"
        verbose_name_plural = "Cutting Recipies"
