from django.shortcuts import redirect


def verify_staff_status(backend, user, response, *args, **kwargs):
    """
    Allows only staff members (is_staff and is_superuser) to log in via Google OAuth.
    Redirects unauthorized users back to the login page with an error message.
    """
    if not (user and user.is_staff and user.is_superuser):
        return redirect('two_factor:profile')
