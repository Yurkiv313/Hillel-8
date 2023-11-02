from django import forms

from Cars.models import OrderQuantity, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["dealership", "client"]


class OrderQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderQuantity
        fields = ["car", "quantity", "order"]
