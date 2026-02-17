import httpx
from typing import Optional


class HTTPClientManager:
    """
    Singleton HTTP client manager with connection pooling.
    Reuses connections for better performance and prevents leaks.
    """
    _client: Optional[httpx.AsyncClient] = None
    
    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        """Get or create shared HTTP client with connection pooling."""
        if cls._client is None:
            cls._client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(
                    max_connections=100,
                    max_keepalive_connections=20
                ),
                http2=True,  # Enable HTTP/2
                follow_redirects=True
            )
        return cls._client
    
    @classmethod
    async def close(cls):
        """Close HTTP client (call on shutdown)."""
        if cls._client:
            await cls._client.aclose()
            cls._client = None


# Singleton instance
http_client_manager = HTTPClientManager()
