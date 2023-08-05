from django.contrib import auth as django_auth
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin

from dbmi_client.settings import dbmi_settings
from dbmi_client import authn

# Get the app logger
logger = dbmi_settings.get_logger()


class DBMIAuthenticationMiddleware(MiddlewareMixin):
    """
    Before loading cached user objects, we want to double-check the JWT to:
    1. Ensure it exists still
    2. Ensure it belongs to the currently cached user
    If any of the above do not pass, do the logout routine

    This middleware is a hybrid of purely JWT authentication and session authentication. The
    initial authentication is performed by inspecting the JWT and then loading/creating the user.
    That user's pk is cached exactly how normal session auth works, and is then consulted from there
    on out to load that user to each request. Once the session expires, the JWT is then looked at
    again to provide authentication. Also, the JWT is still consulted on every request to make sure
    the current user is matched to the current JWT. This check is simply comparing the JWT username/email
    to that of the user instance. If a user session exists and the JWT was swapped for some reason,
    this will detect that change and invalidate the current user session and require another initial
    authentication process.

    When you would use this middleware: This is ideal for instances in which the authentication process
    does some heavy or involved work. If authenticating depends on requests being made to the authorization
    server or resources being pulled from remote sources, this work would be done for every single request,
    and would not be ideal. Doing it upon first auth, and then using the session to determine if the user
    is current or not, minimizes that work, but still ensures JWT defines authentication state.
    """

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):

        # Check for a token
        token = authn.get_jwt(request)
        if not token:
            return AnonymousUser()

        # Get their username
        username = authn.get_jwt_username(request)

        # Use the usual routine to get the currently cached user
        user = django_auth.get_user(request)
        if user.is_authenticated:
            logger.debug('Found existing User session: {}'.format(username))

            # A cached user is present. We need to double-check JWT user to ensure
            # they are the same as the cached user.
            username = authn.get_jwt_username(request, verify=False)
            email = authn.get_jwt_email(request, verify=False)
            if username and email:
                if not user.username.lower() == username.lower() or not user.email.lower() == email.lower():
                    logger.debug('User session does not match JWT, logging out')

                    # TODO: Figure out if its necessary to person any session invalidation here
                    return AnonymousUser()

        else:
            logger.debug('No existing User, attempting to login: {}'.format(username))

            # No user is logged in but we have a JWT token. Attempt to authenticate
            # the current JWT and if it succeeds, login and cache the user.
            user = django_auth.authenticate(request, token=token)
            if user and user.is_authenticated:
                logger.debug('User has authenticated: {}'.format(username))

                # Store this user in session
                django_auth.login(request, user)

            else:
                logger.debug('User could not be authenticated: {}'.format(username))
                # Whatever token this user has, it's not valid OR their account would/could not
                # be created, deny permission. This will likely be the case for instances where
                # automatic user creation is disabled and a user with a valid JWT is not being
                # granted an account.
                raise PermissionDenied

        return user


class DBMIJWTAuthenticationMiddleware(MiddlewareMixin):
    """
    This middleware does not use any user caching at all. For every request, the JWT, if present, is
    inspected to get the username and/or email and that is used to retrieve and set the user on
    the request object. Instead of caching the user's pk on first authentication and then using that
    to pull the user instance on subsequent requests, this simply authenticates the user on every request.
    Since the session is not used, instances of mismatched session and JWT should not occur. Instead
    of relying on the session to cache the current user, we simply use the JWT to do that.

    When to use this middleware: your site depends on JWT to authenticate and there's nothing heavy about the
    authorization process (syncing user state from other services, fetching authorizations, etc)
    """

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):

        # Check for a token
        token = authn.get_jwt(request)
        if not token:
            return AnonymousUser()

        # Get their username
        username = authn.get_jwt_username(request)

        # Attempt to authenticate the current JWT.
        user = django_auth.authenticate(request, token=token)
        if not user or not user.is_authenticated:
            logger.debug('User could not be authenticated: {}'.format(username))
            # Whatever token this user has, it's not valid OR their account would/could not
            # be created, deny permission. This will likely be the case for instances where
            # automatic user creation is disabled and a user with a valid JWT is not being
            # granted an account.
            raise PermissionDenied

        return user

#
#
#
#
# from django.contrib.auth import load_backend
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.functional import SimpleLazyObject
#
#
# def _get_user(request):
#     if not hasattr(request, '_cached_user'):
#         request._cached_user = get_user(request)
#     return request._cached_user
#
#
# class AuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         assert hasattr(request, 'session'), (
#             "The Django authentication middleware requires session middleware "
#             "to be installed. Edit your MIDDLEWARE%s setting to insert "
#             "'django.contrib.sessions.middleware.SessionMiddleware' before "
#             "'django.contrib.auth.middleware.AuthenticationMiddleware'."
#         ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
#         request.user = SimpleLazyObject(lambda: _get_user(request))
#
#
#
# import inspect
# import re
#
# from django.apps import apps as django_apps
# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured, PermissionDenied
# from django.middleware.csrf import rotate_token
# from django.utils.crypto import constant_time_compare
# from django.utils.module_loading import import_string
# from django.utils.translation import LANGUAGE_SESSION_KEY
#
# from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
#
# SESSION_KEY = '_auth_user_id'
# BACKEND_SESSION_KEY = '_auth_user_backend'
# HASH_SESSION_KEY = '_auth_user_hash'
# REDIRECT_FIELD_NAME = 'next'
#
#
# def load_backend(path):
#     return import_string(path)()
#
#
# def _get_backends(return_tuples=False):
#     backends = []
#     for backend_path in settings.AUTHENTICATION_BACKENDS:
#         backend = load_backend(backend_path)
#         backends.append((backend, backend_path) if return_tuples else backend)
#     if not backends:
#         raise ImproperlyConfigured(
#             'No authentication backends have been defined. Does '
#             'AUTHENTICATION_BACKENDS contain anything?'
#         )
#     return backends
#
#
# def get_backends():
#     return _get_backends(return_tuples=False)
#
#
# def _clean_credentials(credentials):
#     """
#     Clean a dictionary of credentials of potentially sensitive info before
#     sending to less secure functions.
#
#     Not comprehensive - intended for user_login_failed signal
#     """
#     SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature', re.I)
#     CLEANSED_SUBSTITUTE = '********************'
#     for key in credentials:
#         if SENSITIVE_CREDENTIALS.search(key):
#             credentials[key] = CLEANSED_SUBSTITUTE
#     return credentials
#
#
# def _get_user_session_key(request):
#     # This value in the session is always serialized to a string, so we need
#     # to convert it back to Python whenever we access it.
#     return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])
#
#
# def authenticate(request=None, **credentials):
#     """
#     If the given credentials are valid, return a User object.
#     """
#     for backend, backend_path in _get_backends(return_tuples=True):
#         try:
#             inspect.getcallargs(backend.authenticate, request, **credentials)
#         except TypeError:
#             # This backend doesn't accept these credentials as arguments. Try the next one.
#             continue
#         try:
#             user = backend.authenticate(request, **credentials)
#         except PermissionDenied:
#             # This backend says to stop in our tracks - this user should not be allowed in at all.
#             break
#         if user is None:
#             continue
#         # Annotate the user object with the path of the backend.
#         user.backend = backend_path
#         return user
#
#     # The credentials supplied are invalid to all backends, fire signal
#     user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)
#
#
# def login(request, user, backend=None):
#     """
#     Persist a user id and a backend in the request. This way a user doesn't
#     have to reauthenticate on every request. Note that data set during
#     the anonymous session is retained when the user logs in.
#     """
#     session_auth_hash = ''
#     if user is None:
#         user = request.user
#     if hasattr(user, 'get_session_auth_hash'):
#         session_auth_hash = user.get_session_auth_hash()
#
#     if SESSION_KEY in request.session:
#         if _get_user_session_key(request) != user.pk or (
#                 session_auth_hash and
#                 not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
#             # To avoid reusing another user's session, create a new, empty
#             # session if the existing session corresponds to a different
#             # authenticated user.
#             request.session.flush()
#     else:
#         request.session.cycle_key()
#
#     try:
#         backend = backend or user.backend
#     except AttributeError:
#         backends = _get_backends(return_tuples=True)
#         if len(backends) == 1:
#             _, backend = backends[0]
#         else:
#             raise ValueError(
#                 'You have multiple authentication backends configured and '
#                 'therefore must provide the `backend` argument or set the '
#                 '`backend` attribute on the user.'
#             )
#     else:
#         if not isinstance(backend, str):
#             raise TypeError('backend must be a dotted import path string (got %r).' % backend)
#
#     request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
#     request.session[BACKEND_SESSION_KEY] = backend
#     request.session[HASH_SESSION_KEY] = session_auth_hash
#     # if hasattr(request, 'user'):
#     #     request.user = user
#     rotate_token(request)
#     user_logged_in.send(sender=user.__class__, request=request, user=user)
#
#
# def logout(request):
#     """
#     Remove the authenticated user's ID from the request and flush their session
#     data.
#     """
#     # Dispatch the signal before the user is logged out so the receivers have a
#     # chance to find out *who* logged out.
#     user = getattr(request, 'user', None)
#     if not getattr(user, 'is_authenticated', True):
#         user = None
#     user_logged_out.send(sender=user.__class__, request=request, user=user)
#
#     # remember language choice saved to session
#     language = request.session.get(LANGUAGE_SESSION_KEY)
#
#     request.session.flush()
#
#     if language is not None:
#         request.session[LANGUAGE_SESSION_KEY] = language
#
#     if hasattr(request, 'user'):
#         from django.contrib.auth.models import AnonymousUser
#         request.user = AnonymousUser()
#
#
# def get_user_model():
#     """
#     Return the User model that is active in this project.
#     """
#     try:
#         return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
#     except ValueError:
#         raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
#     except LookupError:
#         raise ImproperlyConfigured(
#             "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
#         )
#
#
# def get_user(request):
#     """
#     Return the user model instance associated with the given request session.
#     If no user is retrieved, return an instance of `AnonymousUser`.
#     """
#     from django.contrib.auth.models import AnonymousUser
#     user = None
#     try:
#         user_id = _get_user_session_key(request)
#         backend_path = request.session[BACKEND_SESSION_KEY]
#     except KeyError:
#         pass
#     else:
#         if backend_path in settings.AUTHENTICATION_BACKENDS:
#             backend = load_backend(backend_path)
#             user = backend.get_user(user_id)
#
#             # Verify the session
#             if hasattr(user, 'get_session_auth_hash'):
#                 session_hash = request.session.get(HASH_SESSION_KEY)
#                 session_hash_verified = session_hash and constant_time_compare(
#                     session_hash,
#                     user.get_session_auth_hash()
#                 )
#                 if not session_hash_verified:
#                     request.session.flush()
#                     user = None
#
#     return user or AnonymousUser()
#
#
# def get_permission_codename(action, opts):
#     """
#     Return the codename of the permission for the specified action.
#     """
#     return '%s_%s' % (action, opts.model_name)
#
#
# def update_session_auth_hash(request, user):
#     """
#     Updating a user's password logs out all sessions for the user.
#
#     Take the current request and the updated user object from which the new
#     session hash will be derived and update the session hash appropriately to
#     prevent a password change from logging out the session from which the
#     password was changed.
#     """
#     request.session.cycle_key()
#     if hasattr(user, 'get_session_auth_hash') and request.user == user:
#         request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()
#
