from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path

from django_classified.views import area_upload

urlpatterns = [
    path('', include('django_classified.urls', namespace='django_classified')),
    path('social/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),

    # Create custom login page using default 'registration/login.html' template path
    path('login/', auth_views.LoginView.as_view(template_name='demo/login.html'), name='login'),
    path('email-sent/', TemplateView.as_view(template_name='demo/email_sent.html')),
    path('upload-csv/', area_upload, name="area_upload"),
]
