from django.utils import timezone


def custom_context(request):
    gcurrent_year = str(timezone.now().year)
    gcurrent_month = str(timezone.now().strftime('%B'))

    return {
        'gcurrent_year': gcurrent_year,
        'gcurrent_month': gcurrent_month,
    }