from django.urls import path
from . import views

urlpatterns = [

	path('terms/', views.Terms.as_view(), name='terms'),
	path('help/', views.Help.as_view(), name='help'),

]
