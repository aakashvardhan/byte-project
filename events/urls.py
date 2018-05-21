from django.urls import path,re_path, include

from django.contrib.auth import views as auth_views


from . import views

app_name = 'events'

urlpatterns = [
	path('',views.index, name='index'),
	path('login/',views.log_in, name='login'),
    path('logout/',views.log_out, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('register/',views.register, name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('password/',views.change_password, name='change_password'),
    path('accounts/password_reset/',auth_views.password_reset,name='password_reset'),
    path('accounts/password_reset/done/',auth_views.password_reset_done,name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.password_reset_confirm,name='password_reset_confirm'),
    path('accounts/reset/done/',auth_views.password_reset_complete,name='password_reset_complete'),
    path('dashboard/myevents/',views.event_list,name='event_list'),
    path('dashboard/myevents/create/',views.create_event,name='create_event'),
    path('dashboard/myevents/edit/<int:title_id>', views.edit_event,name='edit_event'),
    path('dashboard/myevents/delete/<int:title_id>',views.delete_event,name='delete_event'),
    path('dashboard/attend/<int:title_id>/',views.attendance,name='attendance'),
    path('dashboard/events_to_attend/',views.my_events,name='my_events'),



]