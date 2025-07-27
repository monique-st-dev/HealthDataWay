from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

class SuccessMessageMixin(FormMixin):
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


from django.contrib import messages



class DeleteMessageMixin:
    delete_message = None

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)

        if self.delete_message:
            messages.error(request, self.delete_message)
        else:
            fallback = f"{obj.__class__.__name__} deleted successfully."
            messages.error(request, fallback)

        return response
