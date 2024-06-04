from django import forms

class CustomCardSelectWidget(forms.widgets.Select):
    template_name = 'custom_widgets/custom_card_select.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
