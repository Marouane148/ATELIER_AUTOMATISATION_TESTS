"""
HTTP client wrapper with timeout, retry et mesure de latence.
"""
import requests
import time
from typing import Dict, Any, Optional, Tuple

class APIClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = 1
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Tuple[int, Dict[str, Any], float]:
        """
        GET request avec retry et mesure latence.
        
        Returns:
            (status_code, json_response, latency_ms)
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            try:
                start = time.time()
                response = requests.get(url, params=params, timeout=self.timeout)
                latency_ms = (time.time() - start) * 1000
                
                try:
                    json_data = response.json()
                except:
                    json_data = {"error": "Invalid JSON response"}
                
                return response.status_code, json_data, latency_ms
            
            except requests.exceptions.Timeout:
                if attempt == self.max_retries:
                    return 408, {"error": "Timeout after retries"}, self.timeout * 1000
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries:
                    return 503, {"error": str(e)}, 1000
        
        return 503, {"error": "Unknown error"}, 1000
