# https://pyjwt.readthedocs.io/en/latest/usage.html#reading-headers-without-validation
# -> we can put the organization/service in the headers itself
from typing import Union

from django.utils.functional import cached_property

import jwt
from rest_framework.exceptions import PermissionDenied

from .models import JWTSecret
from .scopes import Scope

EMPTY_PAYLOAD = {
    'scopes': [],
    'zaaktypes': [],
}


class JWTPayload:

    def __init__(self, encoded: str=None):
        self.encoded = encoded

    def __repr__(self):
        return "<%s: payload=%r>" % (self.__class__.__name__, self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def get(self, attr, *args, **kwargs):
        return self.payload.get(attr, *args, **kwargs)

    @cached_property
    def payload(self) -> dict:
        if self.encoded is None:
            return EMPTY_PAYLOAD

        header = jwt.get_unverified_header(self.encoded)

        try:
            jwt_secret = JWTSecret.objects.get(identifier=header['client_identifier'])
        except (JWTSecret.DoesNotExist, KeyError):
            raise PermissionDenied(
                'Client credentials zijn niet aanwezig',
                code='missing-client-identifier'
            )
        else:
            key = jwt_secret.secret

        # the jwt package does verification against tampering (TODO: unit test)
        payload = jwt.decode(self.encoded, key, algorithms='HS256')

        return payload.get('zds', EMPTY_PAYLOAD)

    def has_scopes(self, scopes: Union[Scope, None]) -> bool:
        """
        Check whether all of the expected scopes are present or not.
        """
        if scopes is None:
            # TODO: should block instead of allow it - we'll gradually introduce this
            return True

        scopes_provided = self.payload['scopes']
        # simple form - needs a more complex setup if a scope 'bundles'
        # other scopes
        return scopes.is_contained_in(scopes_provided)


class AuthMiddleware:

    header = 'HTTP_AUTHORIZATION'

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.extract_jwt_payload(request)
        return self.get_response(request) if self.get_response else None

    def extract_jwt_payload(self, request):
        encoded = request.META.get(self.header)
        request.jwt_payload = JWTPayload(encoded)
