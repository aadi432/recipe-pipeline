import time
import logging

logger = logging.getLogger(__name__)

def retry(exceptions, tries=5, delay=1, backoff=2):
    """
    Retry decorator with exponential backoff.
    
    Args:
        exceptions: Exception or tuple of exceptions to catch.
        tries (int): Number of attempts.
        delay (int): Initial delay in seconds.
        backoff (int): Multiplier for delay.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay

            while _tries > 1:
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    logger.warning(
                        f"{func.__name__} failed with error: {e}. "
                        f"Retrying in {_delay}s... ({_tries - 1} retries left)"
                    )
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff

            # final attempt (let exception raise if fails)
            return func(*args, **kwargs)

        return wrapper
    return decorator
