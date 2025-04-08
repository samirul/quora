import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator:
    """Validates passwords to ensure they meet certain criteria.

    This validator checks if a password contains at least one uppercase letter,
    one lowercase letter, one digit, and one special character.
    """
    def validate(self, password, user=None):
        """Validates the given password.

        Checks if the password meets certain criteria:
        - Contains at least one uppercase letter.
        - Contains at least one lowercase letter.
        - Contains at least one digit.
        - Contains at least one special character.

        Args:
            password (str): The password to validate.
            user (User, optional): The user associated with the password. Defaults to None

        Raises:
            ValidationError: If the password does not meet the criteria.
        """
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter."), code='password_no_upper')
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must contain at least one lower letter."), code='password_no_lower')
        if not re.search(r'\d', password):
            raise ValidationError(_("Password must contain at least one digit."), code='password_no_digit')
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(
                _("Password must contain at least one special character (e.g. @, #, $, %, etc.)."),
                code='password_no_special',
            )
    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter one lower letter and one number.")
