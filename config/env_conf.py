import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
)

environ.Env.read_env('.env')

__all__ = [
    env,
]
