from django.views.generic import FormView, TemplateView, CreateView
from chartjs.views.lines import BaseLineChartView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login
from django.shortcuts import redirect

from .forms import ContactForm, SignUpForm, DatasetUploadForm
from .models import User
from .utils import showCharts, showMaps, showStats, getCredentials, getProviders, getData

from random import randint

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'Thank you for making Gather better!')
        return super(ContactView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error while sending the e-mail')
        return super(ContactView, self).form_invalid(form, *args, **kwargs)

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    def form_valid(self, form, *args, **kwargs):
        user = form.save()
        login(self.request, user)
        return redirect('index')


    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error while creating your account')
        return super(SignUpView, self).form_invalid(form, *args, **kwargs)


class AppendixView(LoginRequiredMixin,TemplateView):
    template_name = 'appendix.html'

class MapsView(LoginRequiredMixin,TemplateView):
    template_name = 'maps.html'

    def get_context_data(self, **kwargs):
        context = super(MapsView, self).get_context_data(**kwargs)
        context['isHubMember'] = getCredentials(self.request.user,showMaps)
        return context


class StatsView(LoginRequiredMixin,TemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context['stats'] = getCredentials(self.request.user,showStats)
        return context

class ChartsView(TemplateView):
    template_name = 'charts.html'

class PlotView(BaseLineChartView):

    def get_labels(self):
        labels = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        ]
        return labels
    
    def get_providers(self):
        if not self.request.user.organisation.isHubMember:
            return getProviders(True, self.request.user)
        else:
            return getProviders(False, self.request.user)

    def get_data(self):
        if not self.request.user.organisation.isHubMember:
            return getData(True, self.request.user)
        else:
            return getData(False, self.request.user)


class DatasetUploadView(LoginRequiredMixin, CreateView):
    form_class = DatasetUploadForm
    success_url = reverse_lazy('upload')
    template_name = "dataset_upload.html"

    def get_form_kwargs(self):
        kwargs = super(DatasetUploadView, self).get_form_kwargs()
        kwargs.update({'request': self.request, 'organisation': self.request.user.organisation})
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        user = form.save()
        messages.success(self.request, 'Success in adding your file')
        return redirect(self.success_url)


    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error while creating your account')
        return super(SignUpView, self).form_invalid(form, *args, **kwargs)