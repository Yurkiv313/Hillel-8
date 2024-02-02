import rest_framework.authtoken.views
from django.urls import path
from Cars import api_views
from Cars.api_views import (
    CarTypeViews,
    CarViews,
    DealershipViews,
    CreateOrderViews,
    OrderDetailViews,
    OrderUpdateViews,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

car_types_search_by_name = CarTypeViews.as_view(
    {
        "get": "search_car_types_by_name"
    }
)
cars_search_by_name = CarViews.as_view(
    {
        "get": "search_cars_by_name"
    }
)
dealerships_search_by_name = DealershipViews.as_view(
    {
        "get": "search_dealerships_by_name"
    }
)




cartypes = CarTypeViews.as_view(
    {
        "get": "get_car_type",
    }
)

cars = CarViews.as_view(
    {
        "get": "get_cars",
    }
)

get_car_by_cartype_id = CarViews.as_view(
    {
        "get": "get_car_by_cartype_id",
    }
)

create_order = CreateOrderViews.as_view(
    {
        "post": "create_order",
    }
)

order_get = OrderDetailViews.as_view({"get": "get_cars_by_basket"})

order_delete = OrderDetailViews.as_view({"delete": "remove_cars_from_basket"})

order_id_confirm = OrderUpdateViews.as_view({"put": "order_id_confirm"})


urlpatterns = [
    path("api/cartype/", CarTypeViews.as_view({"get": "list"}), name="car_types_list"),
    path("api/cartype/search/", car_types_search_by_name, name="search_car_types_by_name"),
    path("api/cars/", CarViews.as_view({"get": "list"}), name="cars_list"),
    path("api/cars/search/", cars_search_by_name, name="search_cars_by_name"),
path("api/dealerships/", DealershipViews.as_view({"get": "list"}), name="dealerships_list"),
    path("api/dealerships/search/", dealerships_search_by_name, name="search_dealerships_by_name"),
    path("api/cars/type/<int:pk>", get_car_by_cartype_id, name="get_car_by_cartype_id"),
    path("api/orders/", create_order, name="create_order"),
    path("api/orders/get/", order_get, name="order_get"),
    path(
        "api/delete/orders/<int:order_id>/cars/<int:car_id>", order_delete, name="order"
    ),
    path("api/orders/<int:pk>", order_id_confirm, name="orders_id_confirm"),
    path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token),
    path(
        "webhook-mono/",
        api_views.MonoAcquiringWebhookReceiver.as_view(),
        name="webhook-mono",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
