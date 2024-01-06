from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.utils import json

from Cars.models import CarType, Car, Dealership, Client, Order, OrderQuantity
from Cars.serializer.serializers import CarTypeSerializer, CarSerializer, CreateOrderSerializer, OrderDetailSerializer, \
    OrderUpdateSerializer


@extend_schema(request=CarTypeSerializer, responses={200: CarTypeSerializer(many=True)})
class CarTypeViews(viewsets.ModelViewSet):
    queryset = CarType.objects.all()

    @action(detail=False)
    def get_car_type(self, request):
        cartypes = CarType.objects.all()
        serializer = CarTypeSerializer(cartypes, many=True)
        return JsonResponse(serializer.data, safe=False)


@extend_schema(request=CarSerializer, responses={200: CarSerializer(many=True)})
class CarViews(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    @action(detail=False)
    def get_cars(self, request):
        cartypes = Car.objects.all()
        serializer = CarSerializer(cartypes, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False)
    def get_car_by_cartype_id(self, request, pk):
        global message
        cars = Car.objects.filter(blocked_by_order_id=None, car_type_id=pk)
        filtered_cars = [car for car in cars if car.car_type_id == pk]
        serializer = CarSerializer(filtered_cars, many=True)
        return JsonResponse(serializer.data, safe=False)


@extend_schema(request=CreateOrderSerializer, responses={200: CreateOrderSerializer()})
class CreateOrderViews(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    @action(detail=False)
    def create_order(self, request):
        data = json.loads(request.body)
        car_id = data.get("car_id")
        dealership = Dealership.objects.filter(available_car_types__car=car_id).first()
        client = Client.objects.first()
        order = Order.objects.create(
            client=client, dealership=dealership, is_paid=False
        )

        car = Car.objects.filter(id=car_id).first()
        OrderQuantity.objects.create(car=car, order=order)

        car = Car.objects.get(id=car_id)
        car.blocked_by_order = order
        car.save()

        car.owner = client
        car.save()

        return JsonResponse(
            {"order_id": order.id, "car_id": car_id, "dealership_id": dealership.id, "client_id": client.id}, safe=False
        )


@extend_schema(request=OrderDetailSerializer, responses={200: OrderDetailSerializer()})
class OrderDetailViews(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    @action(detail=False)
    def get_cars_by_basket(self, request):
        order = OrderQuantity.objects.all()
        serializer = OrderDetailSerializer(order, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=["delete"])
    def remove_cars_from_basket(self, request, order_id, car_id):
        order = Order.objects.filter(id=order_id, is_paid=False)
        car = Car.objects.filter(id=car_id).first()
        OrderQuantity.objects.filter(car=car_id, order=order_id).delete()
        Car.objects.get(id=car_id).unblock()
        return JsonResponse({"message": f"Car with id {car_id} deleted successfully"}, safe=False)


@extend_schema(request=OrderUpdateSerializer, responses={200: OrderUpdateSerializer()})
class OrderUpdateViews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["put"])
    def order_id_confirm(self, request, pk):
        order_quantities = OrderQuantity.objects.filter(order_id=pk).all()

        for order_q in order_quantities:
            Car.objects.filter(id=order_q.car.id).update(blocked_by_order=None, owner=None)

        Order.objects.filter(id=pk, is_paid=False).update(is_paid=True)
        return JsonResponse({"message": f"Order with id {pk} paid successfully"}, safe=False)
