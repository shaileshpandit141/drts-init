from datetime import timedelta
from envconfig import config
from tokenmint.services import TokenMint
from tokenmint.cache import ReplayCache
from tokenmint.settings import Settings


replay_cache = ReplayCache(
    redis_url=config.REDIS_CACHE_LOCATION,
)


account_verification_mint = TokenMint(
    settings=Settings(
        issuer="drts-init.com",
        audience="user",
        purpose="account-verification",
        expiry_duration=timedelta(minutes=60),
    ),
    replay_cache=replay_cache,
)


password_reset_mint = TokenMint(
    settings=Settings(
        issuer="drts-init.com",
        audience="user",
        purpose="password-reset",
        expiry_duration=timedelta(minutes=60),
    ),
    replay_cache=replay_cache,
)
