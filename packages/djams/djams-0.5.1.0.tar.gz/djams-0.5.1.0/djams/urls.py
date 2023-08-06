'''
The bindings for analytical microsites
'''
# pylint: disable=wrong-import-position,wrong-import-order
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'djams'

urlpatterns = [
                # path('', views.launch_app, name='launch-app'),
                re_path(r'login/$', views.signin, name='login'),
                path('appsession', views.appsession, name='appsession'),

                url(r'^userlogout/$', views.logout_redirect, name='userlogout'),
                path('logout/', views.endappsession, name='logout'),                
                path('endappsession', views.endappsession, name='endappsession'),

                url(r'^change-password/$', views.change_password, name='change-password'),
                path('passwordchanged/', views.passwordchanged, name='passwordchanged'),

                path('enquiries/', views.enquirylist, name='enquiries'),
                path('myenquiries/', views.enquirylist, name='myenquiries'),
                path('newenquiry', views.newenquiry, name='new-enquiry'),
                path('status_userenquiry/<pk>', views.status_userenquiry, name='status-userenquiry'),

                path('noaccess', TemplateView.as_view(template_name='djams/noaccess.html'), name='noaccess'),
                path('site-privacy-notice', views.enquirylist, name='site-privacy-notice'),
                path('djams-home-page', views.djams_home_page, name='djams-home-page'),

                path('my-clients/', views.my_clients, name='my-clients'),
                path('client/<pk>/', views.client_select, name='client-select'),
          

]