from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from demo.models import Product, Stock

from demo.serializers import ProductSerializer, StockSerializer


# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.prefetch_related('positions__product')
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['positions__product']
    search_fields = ['address']
