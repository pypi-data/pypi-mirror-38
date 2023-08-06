"""
WidgetApp views
"""
from json import loads

from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from open_widget_framework.models import WidgetInstance, WidgetList
from open_widget_framework.utils import get_widget_class_configurations
from open_widget_framework.widget_class_base import WidgetBase

# TODO: validate with widget list


def get_widget_lists(request):
    """
    API endpoint for returning a list of all WidgetList ids
    """
    return JsonResponse([widget_list['id'] for widget_list in WidgetList.objects.all().values('id')], safe=False)


def get_widget_configurations(request):
    """
    API endpoint for getting all available widget classes and their configurations
    """
    return JsonResponse(get_widget_class_configurations(), safe=False)


class WidgetViewSet(ModelViewSet):
    serializer_class = WidgetBase

    def get_queryset(self):
        return WidgetInstance.objects.filter(widget_list_id=self.kwargs['widget_list_id'])

    def list(self, request, *args, **kwargs):
        return JsonResponse([self.serializer_class(widget).render_with_title() for widget in self.get_queryset()],
                            safe=False)

    def create(self, request, *args, **kwargs):
        """
        API endpoint to create a widget instance on a list after validating the data with a serializer
        class
        """
        super().create(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        API endpoint to delete a specified widget
        """
        super().destroy(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        API endpoint to update the data for a widget instance
        """
        super().update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        API endpoint to partial update a widget
        """
        if 'position' in request.data:
            queryset = self.get_queryset()
            target_pos = max(0, min(queryset.count() - 1, request.data.position))
            target_widget = self.get_object()
            current_pos = target_widget.position

            for widget in self.get_queryset():
                if target_pos >= widget.position > current_pos:
                    widget.position -= 1
                    widget.save()
                elif current_pos > widget.position >= target_pos:
                    widget.position += 1
                    widget.save()

        super().update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
