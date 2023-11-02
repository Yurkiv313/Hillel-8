from django.shortcuts import render, redirect
from django.urls import reverse

from Cars.models import Client, CarType, Car, Dealership, Order, OrderQuantity

car_list = []


def hello(request):
    return render(request, "hello/hello.html")


def car_type(request):
    cartypes = CarType.objects.all()
    return render(request, "cartype/cartype_list.html", {"cartypes": cartypes})


def car(request):
    cars = Car.objects.all()
    return render(request, "car/car_list.html", {"cars": cars})


def audi_car_type(request):
    cartypes = CarType.objects.all()
    return render(request, "cartype/Audi.html", {"cartypes": cartypes})


def bmw_car_type(request):
    cartypes = CarType.objects.all()
    return render(request, "cartype/BMW.html", {"cartypes": cartypes})


def mercedes_car_type(request):
    cartypes = CarType.objects.all()
    return render(request, "cartype/Mercedes.html", {"cartypes": cartypes})


def car_edit(request, pk):
    cars = Car.objects.all()
    filtered_cars = [car for car in cars if car.car_type_id == pk]
    return render(request, "car/car_edit_list.html", {"cars": filtered_cars})


def create_order(request, pk):
    dealership = Dealership.objects.filter(available_car_types__car=pk).first()
    client = Client.objects.first()
    order, creator = Order.objects.get_or_create(
        client=client, dealership=dealership, is_paid=False)

    car = Car.objects.filter(id=pk).first()
    OrderQuantity.objects.create(car=car, order=order)
    car.owner = client
    car.save()
    return redirect(reverse(car_edit, args=[car.car_type_id]))


def basket(request):
    orders = OrderQuantity.objects.all()
    return render(request, "basket/basket_list.html", {'orders': orders})
