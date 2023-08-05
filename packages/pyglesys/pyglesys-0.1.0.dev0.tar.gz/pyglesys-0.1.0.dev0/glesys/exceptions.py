class GlesysException(Exception):
    """General, unspecific GleSYS exception."""


class LoginException(GlesysException):
    """An error occurred during login."""
