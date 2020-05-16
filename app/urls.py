from django.contrib import admin
from django.urls import path, include
from feeds_and_speeds import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'machine', views.MachineViewSet)
router.register(r'tool_vendor', views.ToolVendorViewSet)
router.register(r'tool', views.ToolViewSet)
router.register(r'material_class', views.MaterialClassViewSet)
router.register(r'material', views.MaterialViewSet)
router.register(r'cutting_speed', views.CuttingSpeedsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/', include(router.urls)),
    path('', views.calculator, name='calculator')
]
