from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "common/home-page.html"

class AboutView(TemplateView):
    template_name = 'common/about.html'

class ContactView(TemplateView):
    template_name = 'common/contact.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'common/privacy_policy.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'