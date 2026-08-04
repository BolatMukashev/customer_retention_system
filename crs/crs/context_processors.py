def subscription_info(request):
    if request.user.is_authenticated and hasattr(request.user, 'organization'):
        org = request.user.organization
        return {'subscription_days_left': org.subscription_days_left}
    return {}