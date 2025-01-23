from fastapi import HTTPException

class TokenError(Exception):
    """base exeption for error tokens."""


class TokenMissingExpirationError(TokenError):
    """Error: not exist time active token."""


class TokenExpiredError(TokenError):
    """Error: token spoied."""


class TokenInvalidScopeError(TokenError):
    """Eror: incorrect  type tpken."""


class TokenMissingSubjectError(TokenError):
    """Erro: missing subject (sub) in token."""

