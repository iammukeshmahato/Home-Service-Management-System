from django.urls import path, include
from . import admin_views as views

app_name = "admin_dashboard"

urlpatterns = [
    path("", views.home, name="admin_home"),
    path("employee/create", views.employee, name="employee_create"),
    path("employee", views.employee_list, name="employee"),
    path("employee/<int:employee_id>/edit", views.employee_edit, name="employee_edit"),
    path("employee/<int:employee_id>/delete", views.employee_delete, name="employee_delete"),
    path(
        "employee/application", views.employee_application, name="employee_application"
    ),
    path(
        "employee/application/<int:employee_id>",
        views.employee_application,
        name="employee_application",
    ),
    path(
        "employee/application/<int:employee_id>/verify",
        views.employee_verification,
        name="employee_verification",
    ),


    # customers
    path("customer", views.customer_list, name="customer"),
    path("customer/<int:customer_id>", views.customer_delete, name="customer_delete"),

    # services
    path("service", views.service_list, name="service"),
    path("service/create", views.service, name="service_create"),
    path("service/<int:service_id>", views.service_delete, name="service_delete"),
    path("service/<int:service_id>/edit", views.service_edit, name="service_edit"),

    # inquiries
    path("inquiry", views.inquiry_list, name="inquiry"),
    path("inquiry/read", views.inquiry_read, name="inquiry_read"),
    path("inquiry/<int:id>/read", views.inquiry_read, name="inquiry_read"),

    # FAQs
    path("faq", views.faq_list, name="faq"),
    path("faq/create", views.faq, name="faq_create"),
    path("faq/<int:faq_id>", views.faq_delete, name="faq_delete"),
    path("faq/<int:faq_id>/edit", views.faq_edit, name="faq_edit"),
]
