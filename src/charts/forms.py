from django import forms
from datetime import date

PERIOD_CHOICES = [
    ('day', 'Day'),
    ('week', 'Week'),
    ('month', 'Month'),
]

METRIC_CHOICES = [
    ('sugar', 'Blood sugar'),
    ('pressure', 'Blood pressure'),
    ('pulse', 'Pulse'),
]

class ChartFilterForm(forms.Form):
    period_type = forms.ChoiceField(choices=PERIOD_CHOICES, label='Period', widget=forms.RadioSelect)
    selected_date = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date', 'value': date.today().isoformat()}))
    metrics = forms.MultipleChoiceField(
        choices=METRIC_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Table Metrics',
        required=True,
    )
