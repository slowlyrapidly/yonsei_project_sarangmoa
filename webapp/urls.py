from django.urls import path
from django.contrib.auth import views as auth_views # for Auth

from . import views
app_name = 'webapp'

urlpatterns = [

    #시연
    path('', views.main, name='main'),
    path('webapp/main/',views.main,name='main'),
    path('webapp/notice/',views.notice,name='notice'),
    path('webapp/notice_detail/',views.notice_detail,name='notice_detail'),
    path('webapp/manage/',views.manage,name='manage'),
    path('webapp/login_before/',views.login_before,name='login_before'),
    path('webapp/donate_service/', views.donate_service, name='donate_service'),
    path('webapp/faq/', views.faq, name='faq'),
    path('webapp/header',views.header,name='header'),
    path('webapp/footer', views.footer, name='footer'),

    #흥주
    path('webapp/business_introduce/', views.business_introduce, name='business_introduce'),
    path('webapp/certificate/', views.certificate, name='certificate'),
    path('webapp/event/', views.event, name='event'),
    path('webapp/event_detail/', views.event_detail, name='event_detail'),
    path('webapp/good_example/', views.good_example, name='good_example'),
    path('webapp/mypage/', views.mypage, name='mypage'),

    #승윤
    path('webapp/donate_detail/', views.donate_detail, name='donate_detail'),
    path('webapp/donate_apply/', views.donate_apply, name='donate_apply'),
    path('webapp/donate_category/', views.donate_category, name='donate_category'),
    path('webapp/payment/', views.payment, name='payment'),
    path('webapp/save_product/', views.save_product, name='save_product'),
    path('webapp/donation_success/', views.donation_success, name='donation_success'),

    #나
    path('webapp/login/',views.login_view, name='login'),
    path('webapp/signup/', views.signup_view, name='signup'),
    path('webapp/logout/', views.logout_view, name='logout'),
    path('webapp/clear_message/', views.clear_message, name='clear_message'),
    path('webapp/admin_page/', views.admin_page, name='admin_page'),
    path('approve_user/', views.approve_user, name='approve_user'),
    path('reject_user/', views.reject_user, name='reject_user'),
    path('approve_product/', views.approve_product, name='approve_product'),
    path('reject_product/', views.reject_product, name='reject_product'),
    path('cancel_approval/', views.cancel_approval, name='cancel_approval'),
    path('cancel_rejection/', views.cancel_rejection, name='cancel_rejection'),
    path('get_products/',views.get_products,name='get_products'),
    path('process_payment/',views.process_payment,name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),  # 결제 성공 URL
    path('webapp/manage_events/', views.manage_events, name='manage_events'),
    path('webapp/manage_good_examples/', views.manage_good_examples, name='manage_good_examples'),
    path('webapp/manage_notices/', views.manage_notices, name='manage_notices'),
    path('webapp/notice_detail/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('webapp/update_notice/<int:notice_id>/', views.update_notice, name='update_notice'),
    path('webapp/update_good_example/<int:example_id>/', views.update_good_example, name='update_good_example'),
    path('webapp/update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('webapp/update_product/<int:pid>/', views.update_product, name='update_product'),
    path('webapp/delete_product/<int:pid>/', views.delete_product, name='delete_product'),
    path('webapp/delete_notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('webapp/delete_good_example/<int:example_id>/', views.delete_good_example, name='delete_good_example'),
    path('webapp/delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/apply/', views.event_apply, name='event_apply'),

]

