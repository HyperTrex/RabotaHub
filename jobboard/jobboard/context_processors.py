def language(request):
    user_type = ''
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_type = request.user.profile.user_type

    return {
        'lang': request.session.get('language', 'mk'),
        'user_type': user_type,
    }
