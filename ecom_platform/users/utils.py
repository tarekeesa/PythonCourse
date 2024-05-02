from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(_("The password must contain at least one lowercase letter."), code='no_lower_case')
        if not any(char.isupper() for char in password):
            raise ValidationError(_("The password must contain at least one uppercase letter."), code='no_upper_case')

    def get_help_text(self):
        return _("Your password must contain at least one lowercase and one uppercase letter.")
