from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "common/home-page.html"

class AboutView(TemplateView):
    template_name = 'common/about.html'

class ContactView(TemplateView):
    template_name = 'common/contact.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'common/privacy_policy.html'


class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.role == "doctor":
            return redirect("doctor_dashboard")
        elif request.user.role == "patient":
            return redirect("patient_dashboard")
        else:
            return redirect("home")




def custom_404(request, exception):
   return render(request, '404.html', status=404)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_500(request):
    return render(request, '500.html', status=500)
