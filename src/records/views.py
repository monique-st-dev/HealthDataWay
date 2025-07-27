from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import CardiologyRecord, EndocrinologyRecord
from .forms import CardiologyRecordForm, EndocrinologyRecordForm
from .mixins_messages import SuccessMessageMixin, DeleteMessageMixin


class PatientRequiredMixin(UserPassesTestMixin):
    """Allows access only to users with the patient role"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'patient'


# CREATE
class CardiologyRecordCreateView(SuccessMessageMixin, LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = CardiologyRecord
    form_class = CardiologyRecordForm
    template_name = 'records/cardiology_record_form.html'
    success_url = reverse_lazy('cardiology_records_list')
    success_message = "Cardiology record added successfully."

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)


class EndocrinologyRecordCreateView(SuccessMessageMixin, LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = EndocrinologyRecord
    form_class = EndocrinologyRecordForm
    template_name = 'records/endocrinology_record_form.html'
    success_url = reverse_lazy('endocrinology_records_list')
    success_message = "Endocrinology record added successfully."

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)


# LIST
class CardiologyRecordListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = CardiologyRecord
    template_name = 'records/cardiology_records_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        return CardiologyRecord.objects.filter(patient=self.request.user)


class EndocrinologyRecordListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = EndocrinologyRecord
    template_name = 'records/endocrinology_records_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        return EndocrinologyRecord.objects.filter(patient=self.request.user)


# UPDATE
class CardiologyRecordUpdateView(SuccessMessageMixin, LoginRequiredMixin, PatientRequiredMixin, UpdateView):
    model = CardiologyRecord
    form_class = CardiologyRecordForm
    template_name = 'records/cardiology_record_form.html'
    success_url = reverse_lazy('cardiology_records_list')
    success_message = "Cardiology record updated successfully."

    def get_queryset(self):
        return CardiologyRecord.objects.filter(patient=self.request.user)


class EndocrinologyRecordUpdateView(SuccessMessageMixin, LoginRequiredMixin, PatientRequiredMixin, UpdateView):
    model = EndocrinologyRecord
    form_class = EndocrinologyRecordForm
    template_name = 'records/endocrinology_record_form.html'
    success_url = reverse_lazy('endocrinology_records_list')
    success_message = "Endocrinology record updated successfully."

    def get_queryset(self):
        return EndocrinologyRecord.objects.filter(patient=self.request.user)


# DELETE
class CardiologyRecordDeleteView(DeleteMessageMixin, LoginRequiredMixin, PatientRequiredMixin, DeleteView):
    model = CardiologyRecord
    template_name = 'records/cardiology_record_confirm_delete.html'
    success_url = reverse_lazy('cardiology_records_list')
    delete_message = "Cardiology record deleted successfully."

    def get_queryset(self):
        return CardiologyRecord.objects.filter(patient=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)



class EndocrinologyRecordDeleteView(DeleteMessageMixin, LoginRequiredMixin, PatientRequiredMixin, DeleteView):
    model = EndocrinologyRecord
    template_name = 'records/endocrinology_record_confirm_delete.html'
    success_url = reverse_lazy('endocrinology_records_list')
    delete_message = "Endocrinology record deleted successfully."

    def get_queryset(self):
        return EndocrinologyRecord.objects.filter(patient=self.request.user)

