from .models import Car, Component
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('uid', 'color', 'trip', 'year', 'model', 'vendor')


class CarField(serializers.ModelField):
    def to_representation(self, obj):
        if obj.car:
            return obj.car.data()

    def to_internal_value(self, data):
        if data:
            return Car.objects.get(pk=data)


class ComponentSerializer(serializers.ModelSerializer):
    car = CarField(model_field='car', allow_null=True, required=False)

    class Meta:
        model = Component
        fields = ('uid', 'type', 'number', 'car')
