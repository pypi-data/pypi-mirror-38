from django.conf import settings

def extra_context(request):
    return {
        'app_name': getattr(settings, "ACMIN_APP_NAME"),
        "function_name": getattr(settings, "ACMIN_FUNCTION_NAME"),
    }
