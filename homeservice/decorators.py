# your_app/decorators.py
from functools import wraps
from django.shortcuts import redirect


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                print("redicted from decorator")
                return redirect("login")  # Redirect to the login page

            # Check if the user has the required role
            if request.user.role != required_role:
                return redirect(
                    "access_denied"
                )  # Redirect to an access denied page or handle it accordingly

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # If the user is authenticated, determine their role
        if request.user.is_authenticated:
            role = (
                request.user.role
            )  # Adjust this based on your user model's field for roles

            # Redirect based on the user's role
            if role == "customer":
                return redirect(
                    "customer:customer_home"
                )  # Adjust 'customer:dashboard' to the desired URL for customers
            elif role == "employee":
                return redirect(
                    "employee:employee_home"
                )  # Adjust 'employee:dashboard' to the desired URL for employees

            # Add more role-specific redirects as needed

        # If the user is anonymous, proceed with the original view
        return view_func(request, *args, **kwargs)

    return wrapped_view
