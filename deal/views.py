from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import ImportLog, Deal
from .serializers import ImportLogSerializer


class ImportLogViewSet(ModelViewSet):
    queryset = ImportLog.objects.all()
    serializer_class = ImportLogSerializer
