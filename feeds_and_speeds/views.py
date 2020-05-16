from django.shortcuts import render
from feeds_and_speeds.models import Machine, MaterialClass, Material, ToolVendor, Tool, CuttingSpeeds
from django.core import serializers
from django.http import HttpResponse
from feeds_and_speeds.serializers import MachineSerializer, ToolSerializer, ToolVendorSerializer, MaterialClassSerializer, MaterialSerializer, CuttingSpeedsSerializer
from rest_framework import viewsets
from rest_framework import permissions


# Create your views here.
def calculator(request):
    return render(request, 'calculator.html', {})

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class ToolVendorViewSet(viewsets.ModelViewSet):
    queryset = ToolVendor.objects.all()
    serializer_class = ToolVendorSerializer

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

class MaterialClassViewSet(viewsets.ModelViewSet):
    queryset = MaterialClass.objects.all()
    serializer_class = MaterialClassSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class CuttingSpeedsViewSet(viewsets.ModelViewSet):
    queryset = CuttingSpeeds.objects.all()
    serializer_class = CuttingSpeedsSerializer
