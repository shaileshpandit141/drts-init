from datetime import timedelta
from envconfig import env_settings
from authmint.services import TokenMint
from authmint.cache import ReplayCache
from authmint.settings import Settings

account_verification_mint = TokenMint(
    settings=Settings(
        issuer="drts-init.com",
        audience="user",
        purpose="account-verification",
        expiry_duration=timedelta(minutes=60),
    ),
    replay_cache=ReplayCache(
        redis_url=env_settings.redis.cache_location,
    ),
)
