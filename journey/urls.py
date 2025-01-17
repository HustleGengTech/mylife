from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('',views.Home, name='home'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('profile_details/<int:pk>',views.profile_details, name='profile_details'),
    path('about/',views.About, name='about'),
    path('documents/',views.document, name='documents'),
    path('document_create/',views.document_create, name='document_create'),
    path('documents/view/<int:pk>/', views.document_view, name='document_view'),
    path('documents/edit/<int:pk>/', views.document_edit, name='document_edit'),
    path('documents/delete/<int:pk>/', views.document_delete, name='document_delete'),
    path('profile_information/',views.profile_info, name='profile_info'),
    path('profile_picture/',views.profile_picture_change, name='profile_picture'),
    path('emergency-contacts/', views.emergency_contact_list, name='emergency-contact-list'),
    path('emergency-contacts/add/', views.emergency_contact_add, name='emergency-contact-add'),
    path('emergency-contacts/<int:pk>/edit/', views.emergency_contact_edit, name='emergency-contact-edit'),
    path('emergency-contacts/<int:pk>/delete/', views.emergency_contact_delete, name='emergency-contact-delete'),
    path('settings/',views.settings,name='settings'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('delete/', views.delete_account, name='delete_account'),
    path('contact/',views.Contact, name='contact'),
    path('login/',views.Login, name='login'),
    path('login/',views.logout_user, name='logout'),
    path('register/',views.Register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path("write-feedback/", views.write_feedback, name="write_feedback"),
    path("feedback-history/", views.feedback_history, name="feedback_history"),
    path("delete-feedback/<int:feedback_id>/", views.delete_feedback, name="delete_feedback"),


]