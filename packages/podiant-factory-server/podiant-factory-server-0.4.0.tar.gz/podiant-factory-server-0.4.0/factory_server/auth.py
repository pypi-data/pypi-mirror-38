from api.authentication import AuthenticatorBase
from api.authorisation import AuthoriserBase
from api.exceptions import NotAuthenticatedError
from .models import Machine


class MachineKeyAuthenticator(AuthenticatorBase):
    def authenticate(self, request):
        key = request.META.get('HTTP_AUTHORIZATION', '')

        for machine in Machine.objects.filter(key=key[7:]):
            request.user = machine.creator
            request.machine = machine
            return True

        raise NotAuthenticatedError('Invalid bearer token.')


class BearerAuthoriserBase(AuthoriserBase):
    def is_anonymous(self, user):
        a = user.is_anonymous
        return a() if callable(a) else a

    def authorise(self, request, bundle):
        if self.is_anonymous(request.user):
            raise NotAuthenticatedError('Invalid bearer token.')


class OperationAuthoriser(BearerAuthoriserBase):
    pass


class BundleAuthoriser(BearerAuthoriserBase):
    pass


class ProcessAuthoriser(BearerAuthoriserBase):
    pass
