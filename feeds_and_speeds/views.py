from django.shortcuts import render
from feeds_and_speeds.models import Machine, MaterialClass, Material, ToolVendor, Tool, CuttingSpeeds
from django.core import serializers
from django.http import HttpResponse
from feeds_and_speeds.serializers import MachineSerializer, ToolSerializer, ToolVendorSerializer, MaterialClassSerializer, MaterialSerializer, CuttingSpeedsSerializer, CuttingSpeedsCalculationData
from rest_framework import viewsets, permissions
from rest_framework import generics, mixins, views, response


# Create your views here.
def calculator(request):
    return render(request, 'calculator.html', {})

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]

class ToolVendorViewSet(viewsets.ModelViewSet):
    queryset = ToolVendor.objects.all()
    serializer_class = ToolVendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaterialClassViewSet(viewsets.ModelViewSet):
    queryset = MaterialClass.objects.all()
    serializer_class = MaterialClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

class CuttingSpeedsViewSet(viewsets.ModelViewSet):
    queryset = CuttingSpeeds.objects.all()
    serializer_class = CuttingSpeedsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['material', 'tool']

class CuttingSpeedCalculationView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cutting_speed_id):
        csp = CuttingSpeeds.objects.get(id=cutting_speed_id)
        serializer = CuttingSpeedsCalculationData(csp)
        return response.Response(serializer.data)