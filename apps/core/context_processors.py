from django.conf import settings


def debug_context(request):
    """
    Makes DEBUG available in all templates.
    """
    return {
        "DEBUG": settings.DEBUG,
    }
