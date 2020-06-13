from django.contrib import admin
from django.urls import path, include
from feeds_and_speeds import views
from rest_framework import routers
from django.conf.urls import url


router = routers.DefaultRouter()
# drop downs
router.register(r'machine', views.MachineViewSet)
router.register(r'tool_vendor', views.ToolVendorViewSet)
router.register(r'tool', views.ToolViewSet)
router.register(r'material_class', views.MaterialClassViewSet)
router.register(r'material', views.MaterialViewSet)
router.register(r'cutting_speed', views.CuttingSpeedsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/cutting_speed_calculation_data/<int:cutting_speed_id>/', views.CuttingSpeedCalculationView.as_view()),
    path('', views.calculator, name='calculator')
]
