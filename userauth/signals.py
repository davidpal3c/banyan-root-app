# from django.dispatch import receiver
# from allauth.account.signals import user_logged_in
# from django.conf import settings

# @receiver(user_logged_in)
# def populate_user_profile(request, user, **kwargs):
#     social_account = user.socialaccount_set.filter(provider='google').first()
#     if social_account:
#         extra_data = social_account.extra_data
#         user.google_profile_picture = extra_data.get('picture')
#         user.google_locale = extra_data.get('locale')
#         user.save()
