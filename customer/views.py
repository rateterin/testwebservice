from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Top5, Customer
from .serializers import Top5Serializer


class Top5ViewSet(ReadOnlyModelViewSet):
    queryset = Top5.objects.all()
    serializer_class = Top5Serializer
