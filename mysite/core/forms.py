from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class SetDelayForm(forms.Form):
    delay = forms.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1200)
        ]
    )
