from rest_framework import serializers
from .models import Device, Image
import numpy as np


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    # Se le indica que este campo tan solo sera para escritura, no se enviara como respuesta
    deviceName = serializers.CharField(write_only=True, required=False)
    # Campo para escribir los datos
    data = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Image
        fields = ['id', 'deviceName', 'data', 'average_before_normalization', 'average_after_normalization', 'data_size', 'created_date', 'updated_date']
        # Indicamos que datos no se reciben en la informacion adquirida
        read_only_fields = ['average_before_normalization', 'average_after_normalization', 'data_size', 'created_date', 'updated_date']

    """ Validamos que el campo deviceName no este vacio """
    def validate_deviceName(self, value):
        # validamos que el campp deviceName no este vacio
        if not value:
            raise serializers.ValidationError("Need a device name.")
        return value

    """ Validamos la informacion que se encuentra dentro de la key data del JSON """
    def validate_data(self, data):
        try:
            numbers = []
            # Recorremos cada lista de numeros 
            for row in data:
                # Validamos que algunos de los campos de data no este vacio
                if not row:
                    raise serializers.ValidationError("Need a correct data field.")
                # Almacenamos en el array numbers, cada array que se encuentra dentro de data
                numbers.extend([float(num) for num in row.split()])
        except ValueError:
            # Si falla la conversion de algun numero, se envia un mensaje
            raise serializers.ValidationError("All data must be numeric.")
        # Retornamos la lista de valores
        return numbers
    
    """ Creamos un nuevo registro en la base de datos """
    def create(self, information):

        # Se extrae informacion del JSON otorgado
        data = information.pop('data')
        # Se extrae el nombre del dispositivo
        device_name = information.pop('deviceName')
        # Se convierte los datos en un array
        data_array = np.array(data)
        # Se calcular el promedio antes de la normalizacion
        average_before_normalization = np.mean(data_array)
        # Se obtiene un conteo del maximo total alcanzdo en el array
        max_value = np.max(data_array)
        # Se normalizan los datos
        normalized_data = data_array / max_value
        # Se calcular el promedio despues de la normalizacion
        average_after_normalization = np.mean(normalized_data)
        # Se obtiene el disposituvo o crea uno nuevo
        device, _ = Device.objects.get_or_create(device_name=device_name)

        # Se crea el registro
        image = Image.objects.create(
            id = information.pop('id'),
            device = device,
            average_before_normalization = average_before_normalization,
            average_after_normalization = average_after_normalization,
            data_size = len(data)
        )

        return image

        