"""sos_calc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, register_converter
from django.contrib.auth import views

from calc.views import account_router, new_account, select_account, day_router, feature_router, speedups, login_form
from calc.converters import IsoToDayConverter


register_converter(IsoToDayConverter, 'date')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_router),
    path('<int:account_id>/', day_router, name='day_router'),
    path('<int:account_id>/<date:day>/', feature_router, name='feature_router'),
    path('<int:account_id>/<date:day>/speedups', speedups),
    path('accounts/login/', login_form, name="login"),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/new/', new_account, name='new_account'),
    path('accounts/select/', select_account, name='select_account'),
]
