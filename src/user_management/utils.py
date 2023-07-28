import hashlib

from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class InnerIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if (
            request.headers.get('X-INNER-AUTHORIZATION')
            in settings.INNER_AUTHORIZATION_KEYS
        ):
            return super().has_permission(request, view)
        else:
            return False


def hash_user_id(user_id):
    # hash and re-hash
    hashed_user_id = hashlib.sha256(user_id.encode('utf-8')).hexdigest()
    rehashed_user_id = hashlib.sha256(
        hashed_user_id.encode('utf-8')
    ).hexdigest()

    return rehashed_user_id
