from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField(help_text="Length in cm")
    width = models.FloatField(help_text="Width in cm")
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")

    @property
    def volume(self):
        return self.length * self.width * self.height

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm, {self.weight}kg)"

class ShippingBox(models.Model):
    name = models.CharField(max_length=100)
    internal_length = models.FloatField(help_text="Internal length in cm")
    internal_width = models.FloatField(help_text="Internal width in cm")
    internal_height = models.FloatField(help_text="Internal height in cm")
    max_weight_capacity = models.FloatField(help_text="Max weight in kg")
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost in USD")

    @property
    def internal_volume(self):
        return self.internal_length * self.internal_width * self.internal_height

    def __str__(self):
        return f"{self.name} - ${self.cost}"
class Box(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    max_weight = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm)"