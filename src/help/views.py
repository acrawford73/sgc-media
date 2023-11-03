from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HelpView(TemplateView):
	template_name = 'help/index.html'
