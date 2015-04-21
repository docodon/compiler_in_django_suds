from django.conf.urls import patterns , url
from django.views.generic import TemplateView
from compile import views

urlpatterns=patterns('',url(r'^$',views.home,name='home'),
                     url(r'^output2/$', TemplateView.as_view(template_name='output2.html'), name="output2"),
                     ) 