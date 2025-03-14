from django.db import models

# Model's Device 
class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    device_name = models.CharField(max_length=200)

    def __str__(self):
        return self.id, self.device_name

# Model'sImage
class Image(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    average_before_normalization = models.FloatField()
    average_after_normalization = models.FloatField()
    data_size = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
