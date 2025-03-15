from rest_framework import serializers
from .models import Device, Image
import numpy as np


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    # Llamamos al campo device para mostrarlo en las respuestas
    device = DeviceSerializer(read_only=True)
    # Indicamos que este campo no es obligatorio
    id =  serializers.CharField(required=False)
    # Se le indica que este campo tan solo sera para escritura, no se enviara como respuesta
    deviceName = serializers.CharField(write_only=True, required=False)
    # Campo para escribir los datos
    data = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Image
        fields = ['id', 'device', 'deviceName', 'data', 'average_before_normalization', 'average_after_normalization', 'data_size', 'created_date', 'updated_date']
        # Indicamos que datos no se reciben en la informacion adquirida
        read_only_fields = ['average_before_normalization', 'average_after_normalization', 'data_size', 'created_date', 'updated_date']

    def validate(self, attrs):
        # Se obtiene el request de la solicitud
        request = self.context.get('request')

        # Validamos que exista informacion en el request y que la peticion sea tipo POST
        if request and request.method == "POST":
            id = attrs.get('id')
            # Validamos que exista id en el request
            if not id:
            # Retornamos un mensaje de error a la peticion
                raise serializers.ValidationError({"id": "ID is necesary to create."})
            # Validamos que non haya otro campo con este id
            if Image.objects.filter(id=id).exists():
                raise serializers.ValidationError({"id": "Existing record with this id."})
            
            device_name = attrs.get('deviceName')
            if not device_name:
                raise serializers.ValidationError({"deviceName": "Need a device name."})

        return attrs

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
        
    def calculate_before_normalization(self, average):
        # Se retorna el calculo del promedio antes de la normalizacion
        return np.mean(average)
    
    def calculate_after_normalization(self, average):
        # Se obtiene un conteo del maximo total alcanzdo
        max_value = np.max(average)
        # Se normalizan los datos
        normalized_data = average / max_value
        # Se retorna el calculo del promedio despues de la normalizacion
        return np.mean(normalized_data)
    
    """ Creamos un nuevo registro en la base de datos """
    def create(self, information):

        # Se extrae informacion del JSON otorgado
        data = information.pop('data')
        # Se extrae el nombre del dispositivo
        device_name = information.pop('deviceName')
        # Se convierte los datos en un numpy array
        data_array = np.array(data)
        # Se obtiene el disposituvo o crea uno nuevo
        device, _ = Device.objects.get_or_create(device_name=device_name)

        # Se crea el registro
        image = Image.objects.create(
            id = information.pop('id'),
            device = device,
            average_before_normalization = self.calculate_before_normalization(data_array),
            average_after_normalization = self.calculate_after_normalization(data_array),
            data_size = len(data)
        )

        return image
    
    """ Actualizamos un registro existente """
    def update(self, instance, information):

        # Validamos que exista un id nuevo en lo solicitado
        new_id = information.get('id')
        # Validamos si hay id nuevo y si este es diferente al ya almacenado
        if new_id and new_id != instance.id:
            # Informamos que no puede haber ids diferentes
            raise serializers.ValidationError({"id": "Cannot change the ID of an existing record."})

        # Instanciamos si en el request de la solicitud existe algun nombre de dispositivo
        device_name = information.pop("deviceName", None)
        # Validamos si existe instancia 
        if device_name:
            # Capturamos el nombre
            device, _ = Device.objects.get_or_create(device_name=device_name)
            # Instanciamos este nombre
            instance.device = device
        
        # Se valida si el request contiene id
        instance.id = information.get('id', instance.id)

        # Se valida que el objeto contengo algun campo data
        data = information.pop("data", None)
        # Validamos si data contiene algun valor
        if data:
            # Convertimos los datos en un numpy array
            data_array = np.array(data)
            
            # Instanciamos estos nuevos valores y calculamos nuevamente por si existe algun cambio
            instance.average_before_normalization = self.calculate_before_normalization(data_array)
            instance.average_after_normalization = self.calculate_after_normalization(data_array)
            instance.data_size = len(data)

        # Se guardan los cambios
        instance.save()
        return instance

        