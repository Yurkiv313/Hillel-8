from rest_framework import serializers
from Cars.models import CarType, Car, Dealership


class CarTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarType
        fields = ["id", "name", "brand", "price"]


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "color", "year", "car_type_id"]


class CreateOrderSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()


class OrderDetailSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    order_id = serializers.IntegerField()


class OrderUpdateSerializer(serializers.Serializer):
    pass


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = '__all__'
