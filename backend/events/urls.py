from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventList.as_view(), name='events'),
    # Place 'event_create' url before 'event_detail' url -> Reason unknown
    path('create-event/', views.EventCreate.as_view(), name='event_create'),
    # path('<slug>/', views.EventDetail.as_view(), name='event_detail'),  #### Event detail page no longer required
    path('modify-registration/<pk>/', views.modify_registration, name='modify_event_registration'),
    path('modify-event/<slug>/', views.EventUpdate.as_view(), name='event_update'),
    path('delete-event/<slug>/', views.delete_event, name='event_delete'),
    path('modify-event-truncate-num/<pk>/', views.modify_descr_truncate_num, name='modify_event_descr_truncate_num'),
    path('modify-event-truncated-descr/<pk>/', views.modify_truncated_descr, name='modify_event_truncated_descr'),
]
