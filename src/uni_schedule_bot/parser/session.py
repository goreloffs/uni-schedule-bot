import httpx

def create_client(follow_redirects: bool = True, timeout: float = 10.0) -> httpx.Client:
    return httpx.Client(
        follow_redirects=follow_redirects,
        timeout=timeout
    )       