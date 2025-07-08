from .common.client import SearchClient
from .exceptions import handle_search_exceptions

def create_search_client(__credentials__: dict = None) -> SearchClient:
    """
    Create a search client for Elasticsearch.
    
    Args:
        __credentials__: Dictionary of credentials to use.
        
    Returns:
        A search client instance
    """
    if not __credentials__:
        raise ValueError("Missing credentials")

    es_url = __credentials__.get("ES_URL")
    api_key = __credentials__.get("ES_API_KEY")

    if not es_url or not api_key:
        raise ValueError("ES_URL and ES_API_KEY are required in credentials")

    config = {
        "hosts": [es_url],
        "api_key": api_key,
        "verify_certs": str(__credentials__.get("ELASTICSEARCH_VERIFY_CERTS", "true")).lower() == "true"
    }
            
    return SearchClient(config, "elasticsearch")

__all__ = [
    'create_search_client',
    'handle_search_exceptions',
    'SearchClient',
]
