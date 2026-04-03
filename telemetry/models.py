from django.db import models


class SensorReading(models.Model):
    SENSOR_CHOICES = [
        ('proximity', 'Proximity'),
        ('line', 'Line Following'),
        ('camera', 'Camera'),
        ('motor', 'Motor'),
        ('heartbeat', 'Heartbeat'),
        ('system', 'System'),
    ]

    sensor_type = models.CharField(max_length=50, choices=SENSOR_CHOICES)
    value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    topic = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='normal')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sensor_type} | {self.value} {self.unit} | {self.created_at}"