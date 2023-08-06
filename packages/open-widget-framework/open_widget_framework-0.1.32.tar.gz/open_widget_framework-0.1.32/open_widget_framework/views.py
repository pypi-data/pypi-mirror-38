"""
WidgetApp views
"""
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from open_widget_framework.models import WidgetInstance, WidgetList
from open_widget_framework.widget_serializer import WidgetSerializer, WidgetListSerializer, \
    get_widget_class_configurations

# TODO: validate with widget list

def get_widget_configurations(request):
    """
    API endpoint for getting all available widget classes and their configurations
    """
    return JsonResponse({'widgetClassConfigurations': get_widget_class_configurations()})


def make_widget_list_response(queryset):
    return JsonResponse([WidgetSerializer(widget).render_with_title() for widget in queryset], safe=False)


class WidgetListViewSet(ModelViewSet):
    queryset = WidgetList.objects.all()
    serializer_class = WidgetListSerializer

    def list(self, request, *args, **kwargs):
        return JsonResponse([widget_list.id for widget_list in self.queryset], safe=False)

    def retrieve(self, request, *args, **kwargs):
        return make_widget_list_response(self.get_object().get_widgets())

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class WidgetViewSet(ModelViewSet):
    serializer_class = WidgetSerializer

    def get_queryset(self):
        return WidgetInstance.objects.filter(widget_list_id=self.kwargs['widget_list_id']).order_by('position')

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return JsonResponse({
            'widgetClassConfigurations': {
                serializer.data['widget_class']: get_widget_class_configurations()[serializer.data['widget_class']],
            },
            'widgetData': serializer.get_form_data(),
        })

    def create(self, request, *args, **kwargs):
        """
        API endpoint to create a widget instance on a list after validating the data with a serializer
        class
        """
        super().create(request, *args, **kwargs)
        return make_widget_list_response(self.get_queryset())

    def destroy(self, request, *args, **kwargs):
        """
        API endpoint to delete a specified widget
        """
        widget_to_delete = self.get_object()
        for widget in self.get_queryset().filter(position__gt=widget_to_delete.position):
            widget.position -= 1
            widget.save()
        self.perform_destroy(widget_to_delete)
        return make_widget_list_response(self.get_queryset())

    def update(self, request, *args, **kwargs):
        """
        API endpoint to update the data for a widget instance
        """
        #TODO implement?
        super().update(request, *args, **kwargs)
        return make_widget_list_response(self.get_queryset())

    def partial_update(self, request, *args, **kwargs):
        """
        API endpoint to partial update a widget
        """
        if 'position' in request.data:
            queryset = self.get_queryset()
            target_pos = max(0, min(queryset.count() - 1, request.data['position']))
            target_widget = self.get_object()
            current_pos = target_widget.position

            for widget in self.get_queryset():
                if target_pos >= widget.position > current_pos:
                    widget.position -= 1
                    widget.save()
                elif current_pos > widget.position >= target_pos:
                    widget.position += 1
                    widget.save()

        super().partial_update(request, *args, **kwargs)
        return make_widget_list_response(self.get_queryset())
