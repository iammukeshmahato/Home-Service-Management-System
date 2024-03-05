from django.shortcuts import render, HttpResponse, redirect
import secrets
import string
from .employee_form import MyForm
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

from homeservice.models import (
    Employee,
    Service,
    Inquiry,
    FAQ as Faq,
    Appointment,
    Blog,
    Career,
)
from django.contrib import messages
from django.db.models import Q
from homeservice.decorators import role_required
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .blog_form import BlogPostForm


@role_required("admin")
def home(request):
    customer_count = User.objects.filter(role="customer").count()
    employee_count = Employee.objects.filter(is_verified=True).count()
    service_count = Service.objects.all().count()
    if Appointment.objects.all().count() > 0:
        appointment_last_7_days = Appointment.objects.filter(
            date__gte=Appointment.objects.last().date - timedelta(days=7)
        ).count()
    else:
        appointment_last_7_days = 0
    unread_inquiry = Inquiry.objects.filter(is_read=False).count()
    employee_application = Employee.objects.filter(is_verified=False).count()

    data = {
        "customer_count": customer_count,
        "employee_count": employee_count,
        "service_count": service_count,
        "appointment_last_7_days": appointment_last_7_days,
        "unread_inquiry": unread_inquiry,
        "employee_application": employee_application,
    }

    return render(request, "admin/dashboard.html", data)


# create employee
@role_required("admin")
def employee(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        job_title = request.POST.get("service")
        experience = request.POST.get("experience")
        bio = request.POST.get("bio")
        previous_work = request.POST.get("previous_work")
        previous_experience = request.POST.get("previous_experience")

        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))

        print("password=", password)
        form = MyForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # send password to email
                subject = "Login Credentials"
                message = "email: " + email + "\npassword: " + password
                from_email = "iammukeshmahato123@gmail.com"
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print(f"Sorry, employee for the given email {email} can't be created.")

                # print("Sorry employee for given {email} can't be created")
                messages.error(
                    request,
                    f"Sorry, employee for the given email {email} can't be created.",
                )
                # return redirect("admin_dashboard:employee_create")

            # if mail sent successfully then create user
            user = User.objects.create_user(
                email=email,
                fullname=fullname,
                address=address,
                phone=phone,
                profile_pic=request.FILES["profile_pic"],
                role="employee",
                # is_account_verified=True,
            )
            user.set_password(password)
            print("user created successfully")
            employee = Employee.objects.create(
                user=user,
                job_title=Service.objects.get(id=job_title),
                experience=experience,
                bio=bio,
                previous_work=previous_work,
                previous_experience=previous_experience,
                id_type=request.POST.get("id_type"),
                id_image=request.FILES["picture_of_id"],
                is_verified=True,
                is_doc_uploaded=True,
            )
            if employee:
                user.is_account_verified = True
                user.save()
                print("employee created successfully")
                messages.success(request, "Employee added successfully")
            return redirect("admin_dashboard:employee_create")
        else:
            services = Service.objects.all()
            return render(
                request,
                "admin/employee_create.html",
                {"form": form, "services": services},
            )

    services = Service.objects.all()
    return render(request, "admin/employee_create.html", {"services": services})


# view employee
@role_required("admin")
def employee_list(request):
    if request.method == "POST":
        search_text = request.POST.get("search")
        print("search_text=", search_text)
        employees = Employee.objects.filter(
            Q(is_verified=True)
            & (
                Q(user__fullname__istartswith=search_text)
                | Q(user__email__istartswith=search_text)
                | Q(user__phone__istartswith=search_text)
                | Q(user__address__istartswith=search_text)
                | Q(user__email__iexact=search_text)
            )
        )
        return render(
            request,
            "admin/employee.html",
            {"employees": employees, "search_text": search_text},
        )

    employees = Employee.objects.filter(is_verified=True)
    return render(request, "admin/employee.html", {"employees": employees})


# employee application
@role_required("admin")
def employee_application(request, employee_id=None):
    if employee_id:
        employee = Employee.objects.get(id=employee_id)
        # return HttpResponse(employee.user.fullname)
        return render(
            request, "admin/employee_verification.html", {"employee": employee}
        )

    employees = Employee.objects.filter(is_verified=False)
    return render(
        request, "admin/employee_applications_list.html", {"employees": employees}
    )


# view employee application
# @role_required('admin')
# def employee_application(request, employee_id):
#     employee = Employee.objects.get(id=employee_id)
#     return HttpResponse(employee.user.fullname)
#     # return render(request, "admin/employee_application.html", {"employee": employee})


# employee verification
@role_required("admin")
def employee_verification(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == "POST":
        employee.is_verified = True
        employee.save()
        employee.user.is_account_verified = True
        employee.user.save()
        messages.success(request, "Employee verified successfully")
        return redirect("admin_dashboard:employee_application")


# employee edit
@role_required("admin")
def employee_edit(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == "POST":
        print(request.POST)
        employee.user.fullname = request.POST.get("fullname")
        employee.user.address = request.POST.get("address")
        # employee.user.gender = request.POST.get("gender")
        employee.job_title = Service.objects.get(id=request.POST.get("service"))
        employee.experience = request.POST.get("experience")
        employee.id_type = request.POST.get("id_type")
        employee.bio = request.POST.get("bio")
        employee.previous_work = request.POST.get("previous_work")
        employee.previous_experience = request.POST.get("previous_experience")
        if request.FILES.get("profile_pic"):
            employee.user.profile_pic = request.FILES["profile_pic"]
        if request.FILES.get("picture_of_id"):
            employee.id_image = request.FILES["picture_of_id"]
        employee.user.save()
        employee.save()

        messages.success(request, "Employee updated successfully")
        return redirect("admin_dashboard:employee")

    services = Service.objects.all()
    return render(
        request,
        "admin/employee_create.html",
        {"employee": employee, "services": services},
    )
    return HttpResponse("Employee edit page")


# employee delete
@role_required("admin")
def employee_delete(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.user.delete()
    employee.delete()
    messages.success(request, "Employee deleted successfully")
    return redirect("admin_dashboard:employee")


# view customer
@role_required("admin")
def customer_list(request):
    if request.method == "POST":
        search_text = request.POST.get("search")
        customers = User.objects.filter(
            Q(role="customer")
            & (
                Q(fullname__istartswith=search_text)
                | Q(email__istartswith=search_text)
                | Q(phone__istartswith=search_text)
                | Q(address__istartswith=search_text)
                | Q(email__iexact=search_text)
            )
        )
        return render(
            request,
            "admin/customer.html",
            {"customers": customers, "search_text": search_text},
        )

    customers = User.objects.filter(role="customer")
    return render(request, "admin/customer.html", {"customers": customers})


@role_required("admin")
def customer_delete(request, customer_id):
    customer = User.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, "Customer deleted successfully")
    return redirect("admin_dashboard:customer")


# view services
@role_required("admin")
def service_list(request):
    if request.method == "POST":
        search_text = request.POST.get("search")
        services = Service.objects.filter(
            Q(name__istartswith=search_text)
            | Q(description__icontains=search_text)
            | Q(name__iexact=search_text)
        )
        return render(
            request,
            "admin/service.html",
            {"services": services, "search_text": search_text},
        )

    services = Service.objects.all()
    return render(request, "admin/service.html", {"services": services})


# delete service
@role_required("admin")
def service_delete(request, service_id):
    service = Service.objects.get(id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully")
    return redirect("admin_dashboard:service")


# create service
@role_required("admin")
def service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES["image"]

        service = Service.objects.create(
            name=name, description=description, image=image
        )
        messages.success(request, "Service added successfully")
        return redirect("admin_dashboard:service")

    return render(request, "admin/service_create.html")


# edit service
@role_required("admin")
def service_edit(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == "POST":
        service.name = request.POST.get("name")
        service.description = request.POST.get("description")
        if request.FILES.get("image"):
            service.image = request.FILES["image"]
        service.save()
        messages.success(request, "Service updated successfully")
        return redirect("admin_dashboard:service")

    return render(request, "admin/service_create.html", {"service": service})


# view inquiries
@role_required("admin")
def inquiry_list(request):
    inquirys = Inquiry.objects.filter(is_read=False)
    return render(request, "admin/inquiry.html", {"inquirys": inquirys})


# read inquiry
@role_required("admin")
def inquiry_read(request, id=None):
    if id:
        inquiry = Inquiry.objects.get(id=id)
        inquiry.is_read = True
        inquiry.save()
        messages.success(request, "Inquiry read successfully")
        return redirect("admin_dashboard:inquiry")

    inquirys = Inquiry.objects.filter(is_read=True)
    message_type = "read"
    return render(
        request,
        "admin/inquiry.html",
        {"inquirys": inquirys, "message_type": message_type},
    )


# FAQs
@role_required("admin")
def faq(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        faq = Faq.objects.create(question=question, answer=answer)
        messages.success(request, "FAQ created successfully")
        return redirect("admin_dashboard:faq")

    return render(request, "admin/faq_create.html")


# view faqs
@role_required("admin")
def faq_list(request):
    faqs = Faq.objects.all()
    return render(request, "admin/faq.html", {"faqs": faqs})


# edit faq
@role_required("admin")
def faq_edit(request, faq_id):
    faq = Faq.objects.get(id=faq_id)
    if request.method == "POST":
        faq.question = request.POST.get("question")
        faq.answer = request.POST.get("answer")
        faq.save()
        messages.success(request, "FAQ updated successfully")
        return redirect("admin_dashboard:faq")

    return render(request, "admin/faq_create.html", {"faq": faq})


# delete faq
@role_required("admin")
def faq_delete(request, faq_id):
    faq = Faq.objects.get(id=faq_id)
    faq.delete()
    messages.success(request, "FAQ deleted successfully")
    return redirect("admin_dashboard:faq")


# view appointments
@role_required("admin")
def appointment_list(request, id=None):
    if id:
        appointment = Appointment.objects.get(id=id)
        appointment.status = "Approved"
        appointment.save()
        messages.success(request, "Appointment Approved Successfully")
        return redirect("admin_dashboard:appointment")

    # appointments = Appointment.objects.all()
    appointments = Appointment.objects.order_by("-date")
    return render(request, "admin/appointments.html", {"appointments": appointments})


# create blog post
@role_required("admin")
def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        blog = Blog.objects.create(title=title, content=content)
        messages.success(request, "Blog created successfully")
        return redirect("admin_dashboard:blog_create")

    form = BlogPostForm()
    title = "Create Blog Post"
    url = reverse("admin_dashboard:blog_create")
    return render(
        request, "admin/blog_create.html", {"form": form, "title": title, "url": url}
    )


@role_required("admin")
def blog_update(request, id):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        blog = Blog.objects.get(id=id)
        blog.title = title
        blog.content = content
        blog.save()
        messages.success(request, "Blog Updated successfully")
        return redirect("admin_dashboard:blog_create")

    blog = Blog.objects.get(id=id)
    form = BlogPostForm(instance=blog)
    title = "Update Blog Post"
    url = reverse("admin_dashboard:blog_update", args=[blog.id])
    return render(
        request,
        "admin/blog_create.html",
        {"form": form, "blog": blog, "title": title, "url": url},
    )


# view applicants
@role_required("admin")
def applicant_list(request):
    applicants = Career.objects.all()
    return render(request, "admin/applicants.html", {"applicants": applicants})


# update profile
@role_required("admin")
def update_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if not request.user.check_password(current_password):
            messages.error(request, "Invalid current password!")
            print("Invalid current password!")
        else:
            if new_password != confirm_password:
                print("Passwords do not match!")
                messages.error(request, "Passwords do not match!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Password updated successfully!")
                print("Password updated successfully!")
        return redirect("admin_dashboard:profile")
    return render(request, "admin/update_profile.html")


@role_required("admin")
def update_profile_pic(request):
    if request.method == "POST":
        request.user.profile_pic = request.FILES["new_pp"]
        request.user.save()
        messages.success(request, "Profile Picture updated successfully!")
        return redirect("admin_dashboard:profile")
