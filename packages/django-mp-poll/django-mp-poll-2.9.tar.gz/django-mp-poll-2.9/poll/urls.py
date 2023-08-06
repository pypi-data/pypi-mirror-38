
from django.urls import path

from poll import views


app_name = 'poll'


urlpatterns = [

    path('latest/', views.get_latest_poll, name='latest'),

    path('vote/', views.VoteView.as_view(), name='vote')

]
