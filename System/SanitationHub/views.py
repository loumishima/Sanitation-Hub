from django.views.generic import FormView, TemplateView, CreateView, UpdateView
from chartjs.views.lines import BaseLineChartView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404

from .forms import ContactForm, SignUpForm, DatasetUploadForm, EditProfileForm
from .models import User
from .utils import showMaps, showStats, getCredentials, getProviders, getData

from random import randint

class IndexView(TemplateView):
    template_name = 'index.html'


class ContactView(FormView):
    '''
    Send a message to gather. To make that full functional, add the email configs to 
    the settings.py file.

    P.S.: Don't push you settings.py file to github with your password, 
    you are really going to regret that.
    '''
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
    '''
    Create a new user. The type of user created will depend on
    what your organisation code is, if your organisation code
    is linked to a hub-member organisation you have all access,
    if your organisation is linked to a non-hub-member organisation,
    you will have limited access, else you have just access to homepage.

    The signup page will not accept not registered organisation codes, add
    a valid one or leave it empty.

    '''
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

    # TODO: Add the studies on the sanitation risk and the risk formula.
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
    '''
    This function doesn't really generate the charts, 
    but just the page where the chart is in, to know
    how to add charts look at the 'PlotView' view.
    '''
    template_name = 'charts.html'

class PlotView(BaseLineChartView):
    '''
    Load a chart inside an HTML div. you need to provide three function to make
    it works get_labels, get_providers and get_data.

    get_labels: plot's x-axis labels.

    get_providers: labels for the type of information you want to show, if more than one,
    just return a list with the names.

    get_data: the dataset with the stats, it has to be the size 'get_providers' x 'get_labels'.
    '''
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
    '''
    Upload a dataset to a database. Before using, check if you add the server information
    on settings.py

    P.S.: Don't push you settings.py file to github with your server password, 
    you are really going to regret that.
    '''
    form_class = DatasetUploadForm
    success_url = reverse_lazy('upload')
    template_name = "dataset_upload.html"

    def get_form_kwargs(self):
        # Pass the request and organisation information to the form
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

class ProfileView(LoginRequiredMixin, UpdateView):
    '''
    Displays user information, where he can update his information on the hub.

    Some fields are not available for change, like e-mail and username.
    '''
    model = User
    form_class = EditProfileForm
    template_name = 'user_update_form.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)