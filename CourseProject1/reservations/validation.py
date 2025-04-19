from django.core.exceptions import ValidationError

class SpecialCharacterValidator:
    def __init__(self,special_characters=" !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"):
        self.special_characters = special_characters

    def validate(self, password, user=None):
        for char in self.special_characters:
            if char in password:
                return None
        raise ValidationError(f"Your password must contain at least one special character from this list: \"{self.special_characters}\"",code="special_characer_required")

    def get_help_text(self):
        return f"Your password must contain at least one special character from this list: \"{self.special_characters}\""