import time
from functools import wraps
from typing import Callable, Any


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """
    Decorator to retry function calls with exponential backoff.
    
    Handles rate limit errors gracefully by waiting and retrying.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Check if it's a rate limit error
                    is_rate_limit = any([
                        "429" in error_str,
                        "quota" in error_str,
                        "rate limit" in error_str,
                        "resourceexhausted" in error_str
                    ])
                    
                    if not is_rate_limit or attempt == max_retries:
                        # Not a rate limit error or max retries reached
                        raise
                    
                    # Extract retry-after time if available
                    retry_after = None
                    if "retry in" in error_str:
                        try:
                            # Parse "retry in 27.286803409s"
                            parts = error_str.split("retry in")[1].split("s")[0]
                            retry_after = float(parts.strip())
                        except:
                            pass
                    
                    wait_time = retry_after if retry_after else min(delay, max_delay)
                    
                    print(f"⚠ Rate limit hit. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    
                    # Exponential backoff for next attempt
                    delay *= exponential_base
            
            raise Exception(f"Max retries ({max_retries}) exceeded")
        
        return wrapper
    return decorator
