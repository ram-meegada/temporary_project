from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CustomerModel

class NewSitemap(Sitemap):
    def items(self):
        return CustomerModel.objects.all() 

    def location(self, obj):
        return reverse('your_model_detail', args=[obj.pk])
