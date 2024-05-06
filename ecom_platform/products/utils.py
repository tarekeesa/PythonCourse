import re
from django.apps import apps
from django.utils.html import escape

def replace_model_placeholders(text):
    # Regex to find placeholders in the format {app_label.ModelName.field_name}
    pattern = re.compile(r'\{(\w+)\.(\w+)\.(\w+)\}')

    def replace_with_model_data(match):
        app_label, model_name, field_name = match.groups()
        try:
            # Dynamically get the model from the app registry
            model = apps.get_model(app_label, model_name)
            instance = model.objects.first()  # Or implement a more specific query
            if not instance:
                return "[Instance not found]"
            value = getattr(instance, field_name, '[Field not found]')
            return escape(str(value))
        except LookupError:
            return '[Model not found]'
        except AttributeError:
            return '[Field not found]'
        except Exception as e:
            return f'[Error: {str(e)}]'

    return pattern.sub(replace_with_model_data, text)
