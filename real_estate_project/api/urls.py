from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from api.sitemaps import NewSitemap
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import reverse, reverse_lazy

sitemaps = {
    'NewSitemap': NewSitemap,  # Add your sitemap class here
}

urlpatterns = [
    url(r'screener/$', RedirectView.as_view(url=reverse_lazy('first', kwargs={'filter_type': 'most-successful'})), name='first'),
    url(r'screener/year/(?P<year>[0-9]+)/$', SecondView.as_view(), name='first'),
    url(r'screener/(?P<filter_type>[&\w_.@+-]+)/$', SecondView.as_view(), name='first'),
    url(r'screener/(?P<filter_type>[&\w_.@+-]+)/(?P<sme_filter>[&\w_.@+-]+)/$', SecondView.as_view(), name='first'),
    url(r'dsfsd/', SecondView.as_view(), name='test'),


    url('test/', Test.as_view(), name='stock_fundamental'),
    url('stock-view/', StockView.as_view(), name='stock_fundamental'),
    url('upload-file/', UploadFileView.as_view(), name='stock_fundamental_UploadFile'),

    url('Tbnm/', Tbnm.as_view(), name='stock_fundamental_UploadFile'),

]

# urlpatterns = [
    # path('listing/', ListingView.as_view(), name='ListingView'),
    # path('add-room/', AddRoomForm.as_view(), name='AddRoomView'),
    # path('login/', LoginUser.as_view(), name='LoginUser'),
    # path('test/', TestApi.as_view(), name='TestApi'),
# ]

# url(r'screener/$', RedirectView.as_view(url=reverse_lazy('recent_ipo_view', kwargs={'filter_type': 'most-successful'})), name='recent_ipo_view'),

