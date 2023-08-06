from rest_framework import serializers
from django.db.models import CharField, URLField

from open_widget_framework.react_fields import ReactCharField, ReactURLField, ReactChoiceField
from open_widget_framework.models import WidgetList, WidgetInstance


class WidgetBase(serializers.ModelSerializer):
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
        form_fields = ('widget_class', 'title')

    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping.update({
            CharField: ReactCharField,
            URLField: ReactURLField,
        })
        self.serializer_choice_field = ReactChoiceField
        super().__init__(*args, **kwargs)

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
        if widget_class_serializer(data=value).is_valid():
            return value
        else:
            #TODO: better error messaging
            raise serializers.ValidationError('Bad configuration')

    def validate_position(self, value):
        #TODO check for proper positioning
        return value

    def render_with_title(self):
        """
        Runs the class's render function and adds on the title. If the render function returns a string, that string
        will be set to the inner HTML of the default renderer. If it returns a dict, that dict will be passed as a
        configuration to a react_renderer which must be specified.
        """
        base_configuration = self.data
        base_configuration.pop('configuration')

        rendered_body = self.get_widget_serializer().render()
        if isinstance(rendered_body, dict):
            base_configuration.update(rendered_body)
        else:
            base_configuration.update({'html': rendered_body})
        return base_configuration

    @classmethod
    def get_configuration_form_spec(cls, widget_class_name):
        """Returns the specifications for the configuration of a widget class"""
        widget_serializer = WidgetInstance.get_widget_class_serializer(widget_class_name)
        widget_base_form_spec = [cls.fields[key].configure_form_spec() for key in cls.Meta.form_fields]
        widget_class_form_spec = [widget_serializer.fields[key].configure_form_spec()
                                  for key in widget_serializer.fields]
        return widget_base_form_spec + widget_class_form_spec

    def get_widget_serializer(self):
        widget_class_serializer = WidgetInstance.get_widget_class_serializer(self.data['widget_class'])
        widget_serializer = widget_class_serializer(data=self.data['configuration'])
        if not widget_serializer.is_valid():
            # TODO: handle error here
            raise Exception
        else:
            return widget_serializer
