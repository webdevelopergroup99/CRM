from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('adminLogin', views.admin_login, name='adminLogin'),
    path('adminLogout', views.admin_logout, name='adminLogout'),
    path('createUser', views.create_user, name='createUser'),
    path('fetchUser', views.fetch_user, name='fetchUser'),
    path('forgot-password/<main_user_type>', views.forgot_password, name='forgot-password'),
    path('validate-fgt-pwd', views.validate_forgot_password, name='validate-fgt-pwd'),
    path('change-password', views.change_password, name='change-password'),
    path('is-admin-verified', views.is_admin_verified, name='is-admin-verified'),
    path('validate-admin', views.validate_admin_before_show, name='validate-admin'),
    path('view-admin-details', views.view_admin_details, name='view-admin-details'),
    path('redirect-adm-login', views.redirect_admin_login, name='redirect-adm-login'),







]
