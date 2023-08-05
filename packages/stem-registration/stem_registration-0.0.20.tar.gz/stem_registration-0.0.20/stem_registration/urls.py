"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from stem_registration.views import RegistrationViewStem


urlpatterns = [
    url(r'^register/', RegistrationViewStem.as_view(), name='stem_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^select2/', include('django_select2.urls'), name='my_select2'),
]
