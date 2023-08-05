from rest_framework import serializers
from django.db.models import ObjectDoesNotExist

from open_widget_framework.react_fields import ReactCharField
from open_widget_framework.models import WidgetList, WidgetInstance


class WidgetBaseToo(serializers.ModelSerializer):
    """
    WidgetBase is the base serializer for a a widget instance. It handles configuration for fields that all widgets have:
        - react_renderer (default: DefaultRenderer
        - title

    A widget class must extend WidgetBase, specify a name, and implement render method that DOES NOT handle the widget
        title. The extended class can also implement pre-configure and post-configure to further manage the
        widget rendering. Widget classes should specify input fields using the React input fields in react_fields
        in order to get proper form generation on the frontend
    """
    class Meta:
        model = WidgetInstance
        fields = '__all__'

    def render(self, request, configuration):
        """Must be implemented in the subclass"""
        raise NotImplementedError

    def pre_configure(self):
        """Pre configure can be used to dynamically load configuration settings at reference / validation time"""
        # Can be overridden by child class
        pass

    def post_configure(self):
        """Configure widget data after serializer instantiation"""
        # Can be overridden by child class
        pass

    def validate_configuration(self, value):
        widget_class_serializer = WidgetInstance.get_widget_class_serializer(self.initial_data['widget_class'])
        if widget_class_serializer(data = value).is_valid():
            return value
        else:
            raise serializers.ValidationError("Field %s had error: %s" %
                                              list(widget_class_serializer.errors.items())[0])

    def validate_position(self, value):
        #TODO check for proper positioning
        return value

    def render_with_title(self, widget_instance, request=None):
        """
        Runs the class's render function and adds on the title. If the render function returns a string, that string
        will be set to the inner HTML of the default renderer. If it returns a dict, that dict will be passed as a
        configuration to a react_renderer which must be specified.
        """
        rendered_body = self.render(request, widget_instance.configuration)
        if isinstance(rendered_body, dict):
            rendered_body.update(
                {
                    "title": widget_instance.title,
                    "position": widget_instance.position,
                    "reactRenderer": self.react_renderer,
                }
            )
            return rendered_body
        else:
            return {
                "title": widget_instance.title,
                "position": widget_instance.position,
                "html": rendered_body,
                "reactRenderer": self.react_renderer,
            }

    def get_configuration_form_spec(self):
        """Returns the specifications for the configuration of a widget class"""
        return [self.fields[key].configure_form_spec() for key in self.fields]
