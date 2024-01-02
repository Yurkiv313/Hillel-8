from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.signing import Signer
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy

from Cars.forms import CarTypeForm
from Cars.models import Client, CarType, Car, Dealership, Order, OrderQuantity
from Cars.templates.registration.forms import UserCreationFormWithEmail


def first(request):
    return render(request, "registration/first.html")


def hello(request):
    return render(request, "hello/hello.html", {"user": request.user})


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
    if request.method == 'POST':
        car_type = CarType.objects.get(id=pk)
        form = CarTypeForm(request.POST, request.FILES, instance=car_type)
        if form.is_valid():
            form.save()
    global message
    cars = Car.objects.filter(blocked_by_order_id=None)
    filtered_cars = [car for car in cars if car.car_type_id == pk]
    return render(request, "car/car_edit_list.html", {"cars": filtered_cars, "pk": pk})


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


def register(request):
    if request.method == "GET":
        form = UserCreationFormWithEmail()
        return render(request, "registration/register.html", {"form": form})

    form = UserCreationFormWithEmail(request.POST)
    if form.is_valid():
        form.instance.is_active = False
        form.save()
        send_activation_email(request, form.instance)
        return redirect("login")
    return render(request, "registration/register.html", {"form": form})


def send_activation_email(request, user: User):
    user_signed = Signer().sign(user.id)
    signed_url = request.build_absolute_uri(f"/activate/{user_signed}")
    send_mail(
        "Subject here",
        "Click here to activate your account: " + signed_url,
        "yurkivandriy02@gmail.com",
        [user.email],
        fail_silently=False,
    )


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("login")


def activate(request, user_signed):
    try:
        user_id = Signer().unsign(user_signed)
    except BaseException:
        return redirect("login")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")
    user.is_active = True
    user.save()
    return redirect("login")


def password_reset(request):
    return render(request, "registration/password_reset_form.html")


def logout_view(request):
    logout(request)
    return redirect("first")


@login_required
def list_users(request):
    users = User.objects.all()
    return render(request, "registration/users.html", {"users": users})
