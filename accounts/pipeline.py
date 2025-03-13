from django.shortcuts import redirect


def verify_staff_status(backend, user, response, *args, **kwargs):
    """
    Allows only staff members (is_staff and is_superuser) to log in via Google OAuth.
    Redirects unauthorized users back to the login page with an error message.
    """
    if not (user and user.is_staff and user.is_superuser):
        return redirect('two_factor:profile')


def social_uid(backend, details, response, *args, **kwargs):
    """
    Custom pipeline step to return the user ID as a string.
    """

    if backend.name == 'microsoft-graph':
        return {"uid": str(response.get("userPrincipalName"))}

    elif backend.name == 'facebook':
        return {"uid": str(response.get("email"))}

    return {"uid": str(backend.get_user_id(details, response))}
