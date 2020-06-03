from feeds_and_speeds.models import Machine, ToolVendor, Tool, MaterialClass, Material, CuttingSpeeds
from rest_framework import serializers

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'spindle_power', 'max_rpm', 'max_cutting_speed']

class ToolVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolVendor
        fields = ['id', 'name']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'vendor', 'name', 'flute_count', 'flute_length', 'diameter', 'fz_factor_at_one_ae', 'vc_factor_at_one_ae', 'description']

class MaterialClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialClass
        fields = ['id', 'name']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_class', 'name', 'kc_1_1', 'mc']

class CuttingSpeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuttingSpeeds
        fields = ['id', 'tool', 'material', 'feed_per_tooth', 'cutting_speed']
