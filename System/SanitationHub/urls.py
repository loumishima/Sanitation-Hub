from django.urls import path, include
from django.contrib import admin

from .views import ContactView, IndexView, SignUpView, MapsView, AppendixView, StatsView,ChartsView, DatasetUploadView, PlotView, ProfileView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contactUs/', ContactView.as_view(), name='contact'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('maps/', MapsView.as_view(), name='maps'),
    path('appendix/', AppendixView.as_view(), name='appendix'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('charts/', ChartsView.as_view(), name='charts'),
    path('plotcharts/', PlotView.as_view(), name='dados'),
    path('upload/', DatasetUploadView.as_view(), name='upload' ),
    path('profile/',ProfileView.as_view(), name='edit_profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)