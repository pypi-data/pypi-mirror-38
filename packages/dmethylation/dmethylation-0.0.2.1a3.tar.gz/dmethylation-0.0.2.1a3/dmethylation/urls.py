from django.urls import path, include
from rest_framework import routers

from . import api
from dmethylation.views import HealthCheck

router = routers.DefaultRouter()
router.register(r'region', api.RegionViewSet)
router.register(r'illuminamethylation450', api.IlluminaMethylation450ViewSet)
router.register(r'cpghastranscriptregions', api.CpGHasTranscriptRegionsViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    path('health/', HealthCheck.as_view(), name='health'),
)
