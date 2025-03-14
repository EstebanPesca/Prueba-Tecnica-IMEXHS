from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Device, Image
from .serializer import DeviceSerializer, ImageSerializer

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

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