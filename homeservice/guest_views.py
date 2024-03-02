from django.shortcuts import render, HttpResponse, redirect
from .forms import MyForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from homeservice.models import Employee, Inquiry, Rating, FAQ, Career, Blog

User = get_user_model()

from homeservice.models import Service
from homeservice.decorators import anonymous_required


# Create your views here.
def home(request):
    services = Service.objects.all()
    FAQs = FAQ.objects.all()
    return render(request, "index.html", {"services": services, "FAQs": FAQs})


def about(request):
    return render(request, "about.html")


def service(request):
    services = Service.objects.all()
    if request.method == "GET" and request.GET.get("search"):
        services = Service.objects.filter(name__icontains=request.GET.get("search"))
    return render(request, "services.html", {"services": services})


def service_details(request, slug, employee_id=None):
    # if employee_id is given, then the user is viewing the profile of a serviceman
    if employee_id:
        employee = Employee.objects.get(id=employee_id)
        reviews = Rating.objects.filter(employee=employee)

        # destructuring the reviews because we need to change the rate to a string so that we can use it in the template to iterate over the stars
        processed_reviews = []
        for review in reviews:
            if review.rate == 1:
                rate = "a"
            elif review.rate == 2:
                rate = "aa"
            elif review.rate == 3:
                rate = "aaa"
            elif review.rate == 4:
                rate = "aaaa"
            elif review.rate == 5:
                rate = "aaaaa"

            review = {
                "pk": review.pk,
                "rate": rate,
                "review": review.review,
                "customer": review.customer,
                "date": review.date,
            }
            processed_reviews.append(review)
            print(review)
        return render(
            request,
            "serviceman.html",
            {"employee": employee, "reviews": processed_reviews},
        )
    service = Service.objects.get(slug=slug)
    employees = Employee.objects.filter(job_title=service.pk, is_verified=True)
    return render(
        request, "service_details.html", {"service": service, "employees": employees}
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")
        inquiry = Inquiry(name=name, email=email, phone=phone, message=message)
        inquiry.save()
        messages.success(
            request,
            "Your inquery form has been submitted successfully. We will contact you soon.",
        )
        return redirect("contact")
    return render(request, "contact.html")


def career(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        cv = request.FILES.get("cv")
        career = Career(name=name, email=email, phone=phone, cv=cv)
        career.save()
        messages.success(
            request,
            "Your CV has been submitted successfully. We will contact you soon.",
        )
        return redirect("career")
    return render(request, "career.html")


@anonymous_required
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
        if user:
            if user.role == "customer":
                login(request, user)
                # return HttpResponse("Customer Home")
                return redirect("customer:customer_home")
            elif user.role == "employee":
                login(request, user)
                if not request.user.is_account_verified:
                    return redirect("employee:employee_register")
                else:
                    print("Login Successful, You are a Employee")
                    return redirect("employee:employee_home")
            elif user.role == "admin":
                login(request, user)
                return redirect("admin_dashboard:admin_home")
        else:
            messages.error(request, "Invalid Email or Password")
            redirect("login")
    return render(request, "login.html")


@anonymous_required
def register_page(request):
    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        contact = request.POST["contact"]
        is_employee = request.POST["is_employee"]
        profile_pic = request.FILES["profile_pic"]
        password = request.POST["password1"]

        form = MyForm(request.POST, request.FILES)

        if form.is_valid():
            if is_employee == "True":
                user = User.objects.create_user(
                    email=email,
                    fullname=name,
                    address=address,
                    phone=contact,
                    profile_pic=profile_pic,
                    role="employee",
                )
                message = "Employee registered successfully"
                messages.success(request, "Employee registered successfully")
            else:
                user = User.objects.create_user(
                    email=email,
                    fullname=name,
                    address=address,
                    phone=contact,
                    profile_pic=profile_pic,
                )
                message = "Customer registered successfully"
                messages.success(request, "Customer registered successfully")
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            return render(request, "register.html", {"form": form})

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return redirect("login")


def complete_profile(request):
    service = Service.objects.all()
    print(service)
    return render(request, "complete_profile.html", {"service": service})


def blog(request):
    posts = Blog.objects.order_by("-created_at")
    return render(request, "blog_list.html", {"posts": posts})


def blog_post(request, slug):
    post = Blog.objects.get(slug=slug)
    return render(request, "post.html", {"post": post})
