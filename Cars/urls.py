from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.first, name="first"),
    path("hello/", views.hello, name="hello"),
    path("cartype/", views.car_type, name="car_type"),
    path("car/", views.car, name="car"),
    path("audict/", views.audi_car_type, name="audi_car_type"),
    path("bmwct/", views.bmw_car_type, name="bmw_car_type"),
    path("mercedesct/", views.mercedes_car_type, name="mercedes_car_type"),
    path("car_edit/<int:pk>", views.car_edit, name="car_edit"),
    path("create_order/<int:pk>", views.create_order, name="create_order"),
    path("basket/", views.basket, name="basket"),
    path("order_cancel/", views.order_cancel, name="order_cancel"),
    path("order_confirm/", views.order_confirm, name="order_confirm"),
    path("redi/", views.redi, name="redi"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.list_users, name="users"),
    path("activate/<user_signed>", views.activate, name="activate"),
    path("password_reset/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password_reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/login/",
        ),
        name="password_reset_confirm",
    ),
]
