from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

from api.views import LenderViewSet, LenderCSV


router = DefaultRouter()
router.register('lenders', LenderViewSet, basename='lender')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lenders/csv/', LenderCSV.as_view(), name="lender-csv"),
]

urlpatterns += router.urls
