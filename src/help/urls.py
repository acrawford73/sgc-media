from django.urls import path, re_path
from . import views

urlpatterns = [

	path('help/', views.HelpView.as_view(), name='help'),

]