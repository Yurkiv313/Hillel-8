from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.utils import json
from rest_framework.views import APIView

from Cars.pagination.limited_pagination import LimitedPagination
from Cars.invoices import create_invoice, verify_signature
from Cars.models import CarType, Car, Dealership, Order, OrderQuantity
from Cars.serializer.serializers import (
    CarTypeSerializer,
    CarSerializer,
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderUpdateSerializer,
    DealershipSerializer,
)


@extend_schema(request=CarTypeSerializer, responses={200: CarTypeSerializer(many=True)})
class CarTypeViews(viewsets.ModelViewSet):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    pagination_class = LimitedPagination

    @action(detail=False)
    def search_car_types_by_name(self, request):
        name_query = self.request.query_params.get('name', '')
        car_types = CarType.objects.filter(name__icontains=name_query)
        serializer = CarTypeSerializer(car_types, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False)
    def get_car_type(self, request):
        cartypes = CarType.objects.all()
        serializer = CarTypeSerializer(cartypes, many=True)
        return JsonResponse(serializer.data, safe=False)


@extend_schema(request=CarSerializer, responses={200: CarSerializer(many=True)})
class CarViews(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = LimitedPagination

    @action(detail=False)
    def search_cars_by_name(self, request):
        name_query = self.request.query_params.get('name', '')
        cars = Car.objects.filter(car_type__name__icontains=name_query)
        serializer = CarSerializer(cars, many=True)
        return JsonResponse(serializer.data, safe=False)

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


class DealershipViews(viewsets.ModelViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    pagination_class = LimitedPagination

    @action(detail=False)
    def search_dealerships_by_name(self, request):
        name_query = self.request.query_params.get('name', '')
        dealerships = Dealership.objects.filter(name__icontains=name_query)
        serializer = DealershipSerializer(dealerships, many=True)
        return JsonResponse(serializer.data, safe=False)


@extend_schema(request=CreateOrderSerializer, responses={200: CreateOrderSerializer()})
class CreateOrderViews(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    @action(detail=False)
    def create_order(self, request):
        data = json.loads(request.body)
        car_id = data.get("car_id")
        dealership = Dealership.objects.filter(available_car_types__car=car_id).first()
        client = request.user
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
            {
                "order_id": order.id,
                "car_id": car_id,
                "dealership_id": dealership.id,
                "client_id": client.id,
            },
            safe=False,
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
        return JsonResponse(
            {"message": f"Car with id {car_id} deleted successfully"}, safe=False
        )


@extend_schema(request=OrderUpdateSerializer, responses={200: OrderUpdateSerializer()})
class OrderUpdateViews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["put"])
    def order_id_confirm(self, request, pk):
        order_quantities = OrderQuantity.objects.filter(order_id=pk).all()

        for order_q in order_quantities:
            Car.objects.filter(id=order_q.car.id).update(
                blocked_by_order=None, owner=None
            )

        order = Order.objects.get(id=pk)
        invoice_url = create_invoice(order, reverse("webhook-mono", request=request))
        return Response({"invoice_url": invoice_url})


class MonoAcquiringWebhookReceiver(APIView):
    serializer_class = OrderUpdateSerializer

    def post(self, request):
        try:
            print("Webhook received 1:", request.data)
            print("Webhook body 1:", request.body)
            print("Webhook headers 1:", request.headers)

            reference = request.data.get("reference")
            print(f"Reference: {reference}")

            order_to_update = Order.objects.filter(id=reference).first()
            if order_to_update:
                print("Order found for update:", order_to_update)
                Order.objects.filter(id=reference).update(is_paid=True)
                print("Order updated successfully.")
            else:
                print("Order not found for update.")

            verify_signature(request)
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return Response({"status": "error"}, status=400)
        return Response({"status": "ok"})
