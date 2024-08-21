from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView


class Terms(TemplateView):
	template_name = 'core/terms.html'

class Help(TemplateView):
	template_name = 'core/help.html'
