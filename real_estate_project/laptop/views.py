from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http import Http404

class Test(View):
    def get(self, request):
        raise Http404