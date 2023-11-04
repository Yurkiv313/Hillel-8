from django.shortcuts import render, redirect
from django.urls import reverse

from Cars.models import Client, CarType, Car, Dealership, Order, OrderQuantity


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
    global message
    cars = Car.objects.filter(blocked_by_order_id=None)
    filtered_cars = [car for car in cars if car.car_type_id == pk]
    return render(request, "car/car_edit_list.html", {"cars": filtered_cars})


def create_order(request, pk):
    dealership = Dealership.objects.filter(available_car_types__car=pk).first()
    client = Client.objects.first()
    order, creator = Order.objects.get_or_create(
        client=client, dealership=dealership, is_paid=False
    )

    car = Car.objects.filter(id=pk).first()
    OrderQuantity.objects.create(car=car, order=order)

    car = Car.objects.get(id=pk)
    car.blocked_by_order = order
    car.save()

    car.owner = client
    car.save()
    return redirect(reverse(car_edit, args=[car.car_type_id]))


def remove_from_cart(request, pk):
    dealership = Dealership.objects.filter(available_car_types__car=pk).first()

    order = Order.objects.filter(
        client=Client.objects.first(), dealership=dealership, is_paid=False
    ).first()

    car_type = CarType.objects.filter(car=pk).first()
    OrderQuantity.objects.delete(car_type=car_type, order=order)
    Car.objects.get(id=pk).unblock()
    return redirect(reverse(car_edit))


def basket(request):
    cars = Car.objects.filter(blocked_by_order__isnull=False)
    return render(request, "basket/basket_list.html", {"cars": cars})


def order_cancel(request):
    orders = Order.objects.filter(client=Client.objects.first(), is_paid=False).all()
    for order in orders:
        Car.objects.filter(
            owner_id__isnull=False, blocked_by_order_id__isnull=False
        ).update(blocked_by_order_id=None, owner_id=None)
        order.delete()

    return render(request, "basket/order_cancel.html")


def order_confirm(request):
    orders = Order.objects.filter(client=Client.objects.first(), is_paid=False).all()
    for order in orders:
        Car.objects.filter(
            owner_id__isnull=False, blocked_by_order_id__isnull=False
        ).update(blocked_by_order_id=None, owner_id=None)
        order.delete()
    return render(request, "basket/order_confirm.html")


def redi(request):
    return redirect(hello)
