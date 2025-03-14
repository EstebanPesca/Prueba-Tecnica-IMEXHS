from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger('django')

from .models import Device, Image
from .serializer import DeviceSerializer, ImageSerializer

# Create your views here.

def custom_exception_handler(exc, context):
    logger.error(f"ERROR: {exc}")
    response = exception_handler(exc, context)
    return response

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

""" Filtros personalizados para obtener informacion """
class ImageFilter(filters.FilterSet):
    # Filtro para obtener fecha de creacion "mayor o menor que o a igual"
    created_date_gte = filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date_lte = filters.DateFilter(field_name="created_date", lookup_expr="lte")
    # Filtro para obtener fecha de actualizacion "mayor o menor que o a igual"
    updated_date_gte = filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date_lte = filters.DateFilter(field_name="updated_date", lookup_expr="lte")
    # Filtro para obtener promedio antes de la normalizacion "mayor o menor que o a igual"
    average_before_normalization_gte = filters.NumberFilter(field_name="average_before_normalization", lookup_expr="gte")
    average_before_normalization_lte = filters.NumberFilter(field_name="average_before_normalization", lookup_expr="lte")
    # Filtro para obtener promedio despues de la normalizacion "mayor o menor que o a igual"
    average_after_normalization_gte = filters.NumberFilter(field_name="average_after_normalization", lookup_expr="gte")
    average_after_normalization_lte = filters.NumberFilter(field_name="average_after_normalization", lookup_expr="lte")
    # Filtro para obtener tamaño "mayor o menor que o a igual"
    data_zise_gte = filters.NumberFilter(field_name="data_size", lookup_expr="gte")
    data_zise_lte = filters.NumberFilter(field_name="data_size", lookup_expr="lte")

    class Meta:
        model = Image
        fields = ['created_date', 'updated_date', 'average_before_normalization', 'average_after_normalization', 'data_size']

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ImageFilter

    def create(self, request, *args, **kwargs):
        
        # Almacenamos el JSON en un variable 
        payload = request.data

        # Procesamos cada elemento
        for key, value in payload.items():
            # Llamamos al serializador con el metodo get_serializer
            serializer = self.get_serializer(data=value)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response({"message":"Data created successfully"}, status=201)
    