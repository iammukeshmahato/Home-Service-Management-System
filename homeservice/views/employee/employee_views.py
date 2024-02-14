from django.shortcuts import HttpResponse, redirect, render
from homeservice.models import Service, Employee


def register(request):
    service = Service.objects.all()
    if Employee.objects.filter(user=request.user).exists():
        employee = Employee.objects.filter(user=request.user)
        return render(request, "employee/complete_profile.html", {"employee": employee})
        return HttpResponse("You have already submitted your documents")

    if request.method == "POST":
        job_title = request.POST.get("job_title")
        experience = request.POST.get("experience")
        bio = request.POST.get("bio")
        id_type = request.POST.get("id_type")
        id_image = request.FILES["id_image"]
        print(job_title, experience, bio, id_type, id_image)

        employee = Employee(
            user=request.user,
            job_title=job_title,
            experience=experience,
            bio=bio,
            id_type=id_type,
            id_image=id_image,
            is_doc_uploaded=True,
        )
        employee.save()

        return HttpResponse("Profile Updated! Wait for approval")

    return render(request, "employee/complete_profile.html", {"service": service})


def home(request):
    return HttpResponse("Employee home")
