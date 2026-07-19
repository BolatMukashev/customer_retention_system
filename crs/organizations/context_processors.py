def organization(request):
    if request.user.is_authenticated:
        return {
            "organization": getattr(request.user, "organization", None)
        }
    return {}