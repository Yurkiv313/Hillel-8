from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("cartype/", views.car_type, name="car_type"),
    path("car/", views.car, name="car"),
    path("audict/", views.audi_car_type, name="audi_car_type"),
    path("bmwct/", views.bmw_car_type, name="bmw_car_type"),
    path("mercedesct/", views.mercedes_car_type, name="mercedes_car_type"),
    path("car_edit/<int:pk>", views.car_edit, name="car_edit"),
    path("create_order/<int:pk>", views.create_order, name="create_order"),
    path("basket/", views.basket, name="basket"),
    # path("order/<int:pk>", views.create_order, name="create_order"),

    # path("form/", views.order_form, name="order_form"),
    # path("quantityform/", views.order_quantity_form, name="order_quantity_form"),
]
