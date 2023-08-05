"""
WidgetApp urls
"""
from django.conf.urls import url
from open_widget_framework.views import (
    WidgetListViewSet,
    WidgetView,
    get_widget_configurations,
)


urlpatterns = [
    url(r"^api/v1/lists$", WidgetListViewSet.as_view({'get': 'list'}), name="get_lists"),
    url(
        r"^api/v1/configurations$", get_widget_configurations, name="get_configurations"
    ),
    url(
        r"^api/v1/list/(?P<widget_list_id>\d*)$",
        WidgetListViewSet.as_view({
            'get': 'retrieve',
            'post': 'create',
            'delete': 'destroy'
        }),
        name="widget_list_view",
    ),
    url(
        r"^api/v1/list/(?P<widget_list_id>\d+)/widget/(?P<widget_id>\d*)$",
        WidgetView.as_view(),
        name="widget_view",
    ),
]
