"""
WidgetApp urls
"""
from django.conf.urls import url
from open_widget_framework.views import (
    WidgetListViewSet,
    WidgetViewSet,
    get_widget_lists,
    get_widget_configurations,
)


urlpatterns = [
    url(r"^api/v1/lists$", get_widget_lists, name="get_lists"),
    url(
        r"^api/v1/configurations$", get_widget_configurations, name="get_configurations"
    ),
    url(
        r"^api/v1/list/(?P<widget_list_id>\d*)$",
        WidgetViewSet.as_view({
            'get': 'list',
        }),
        name="widget_list_view",
    ),
    url(
        r"^api/v1/list/(?P<widget_list_id>\d+)/widget/(?P<pk>\d*)$",
        WidgetViewSet.as_view({
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name="widget_view",
    ),
]
