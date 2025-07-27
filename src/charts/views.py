from django.views.generic import FormView
from .forms import ChartFilterForm
from records.models import EndocrinologyRecord, CardiologyRecord
from datetime import timedelta

class ChartTableView(FormView):
    template_name = 'charts/chart_table.html'
    form_class = ChartFilterForm

    def form_valid(self, form):
        user = self.request.user
        period_type = form.cleaned_data['period_type']
        selected_date = form.cleaned_data['selected_date']
        metrics = form.cleaned_data['metrics']


        if period_type == 'day':
            start_date = end_date = selected_date
        elif period_type == 'week':
            start_date = selected_date - timedelta(days=selected_date.weekday())
            end_date = start_date + timedelta(days=6)
        elif period_type == 'month':
            start_date = selected_date.replace(day=1)
            if selected_date.month == 12:
                end_date = selected_date.replace(year=selected_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = selected_date.replace(month=selected_date.month + 1, day=1) - timedelta(days=1)


        context = self.get_context_data(form=form)
        context['metrics'] = metrics
        context['start_date'] = start_date
        context['end_date'] = end_date


        if 'sugar' in metrics:
            sugar_data = EndocrinologyRecord.objects.filter(
                patient=user,
                date__range=(start_date, end_date)
            ).order_by('date')
            context['sugar_data'] = sugar_data


        if 'pressure' in metrics or 'pulse' in metrics:
            cardio_data = CardiologyRecord.objects.filter(
                patient=user,
                date__range=(start_date, end_date)
            )


            if 'pressure' in metrics and 'pulse' not in metrics:
                cardio_data = cardio_data.exclude(
                    systolic__isnull=True,
                    diastolic__isnull=True,
                )


            elif 'pulse' in metrics and 'pressure' not in metrics:
                cardio_data = cardio_data.exclude(pulse__isnull=True)


            elif 'pressure' in metrics and 'pulse' in metrics:
                cardio_data = cardio_data.exclude(
                    systolic__isnull=True,
                    diastolic__isnull=True,
                    pulse__isnull=True,
                )

            context['cardio_data'] = cardio_data.order_by('date')

        return self.render_to_response(context)
