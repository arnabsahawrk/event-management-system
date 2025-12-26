from django.conf import settings

from apps.core.helpers import is_admin, is_organizer, is_participant


def debug_context(request):
    return {
        "DEBUG": settings.DEBUG,
    }


def user_roles_context(request):
    if request.user.is_authenticated:
        return {
            "user_roles": {
                "is_admin": is_admin(request.user),
                "is_organizer": is_organizer(request.user),
                "is_participant": is_participant(request.user),
            }
        }
    return {
        "user_roles": {
            "is_admin": False,
            "is_organizer": False,
            "is_participant": False,
        }
    }
