from django.urls import path

from . import views
from .views import *

app_name = 'rideshare'
urlpatterns = [
    # User account related
    path('', views.index, name='index'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.login, name='logout'),
    path('accounts/register/', views.register, name='register'),

    # For registered users
    path('home/', views.home, name='home'),
    path('registerdriver/', DriverRegisterView.as_view(), name='registerdriver'),
    path('requestride/', views.ridehome, name='ridehome'),
    path('shareride/', views.sharerhome, name='sharehome'),
    path('ridestatus/',views.ridehisotry,name='ridehistory'),

    # Ride create/share/update for owner/sharer
    path('ride/<int:pk>',RideDetailView.as_view(),name='ride-detail'),
    path('ride/new',RideCreateView.as_view(),name='ride-form'),
    path('ride/<int:pk>/update/',RideUpdateView.as_view(),name='ride-update'),
    path('ride/<int:pk>/delete/',RideDeleteView.as_view(),name='ride-delete'),
    path('shareride/new', SharerCreatelView.as_view(), name='sharer-form'),
    path('shareride/list', views.sharersearchlist, name='sharer-list'),
    path('shareride/<int:pk>/join/', views.sharerjoin, name='sharer-join'),
    path('shareride/<int:pk>/cancel/', views.sharercancel, name='sharer-cancel'),
    path('shareride/<int:pk>', views.sharedetail, name='sharer-detail'),
    path('shareride/<int:pk>/update', views.shareupdate, name='sharer-update'),

    # Driver
    path('driver/', views.driverhome, name='driverhome'),
    path('driver/<int:pk>', DriverDetailView.as_view(), name='driver-detail'),
    path('driver/riderequests', riderequests, name='riderequests'),
    path('driver/driverhistory', driverhistory, name='driverhistory'),
    path('driver/<int:pk>/update/', DriverUpdateView.as_view(), name='driver-update'),
    path('driver/<int:pk>/delete/', DriverDeleteView.as_view(), name='driver-delete'),
    path('driver/riderequests/claimride/<int:pk>', ClaimRideView.as_view(), name='claimride'),
    path('driver/riderequests/completeride/<int:pk>', CompleteRideView.as_view(), name='completeride'),
]
