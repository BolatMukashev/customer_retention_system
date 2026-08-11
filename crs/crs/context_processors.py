def subscription_info(request):
    if request.user.is_authenticated:
        org = getattr(request.user, 'organization', None)
        if org:
            return {'subscription_days_left': org.subscription_days_left}
    return {}