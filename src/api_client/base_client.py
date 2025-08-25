import requests
import time
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import settings


class APIClient:
    """Base API client for Music Catalog API"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or settings.BASE_URL
        self.api_key = api_key or settings.API_KEY
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create configured requests session"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=settings.MAX_RETRIES,
            backoff_factor=settings.RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Music-Catalog-API-Tests/1.0.0"
        })
        
        if self.api_key:
            session.headers["Authorization"] = f"Bearer {self.api_key}"
        
        return session
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=settings.TIMEOUT,
                **kwargs
            )
            
            # Log request/response for debugging
            print(f"Request: {method} {url}")
            if data:
                print(f"Request Data: {data}")
            print(f"Response Status: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request("POST", endpoint, data=data, **kwargs)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request("PUT", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request("DELETE", endpoint, **kwargs)