"""
Tests "as code" : assertions sur contrat, robustesse et QoS.
"""
from typing import Dict, List, Any, Tuple

class TestResult:
    def __init__(self, name: str, status: str, latency_ms: float = 0, details: str = ""):
        self.name = name
        self.status = status  # PASS, FAIL, ERROR
        self.latency_ms = latency_ms
        self.details = details
    
    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "details": self.details
        }

class QuotableTests:
    """Tests pour l'API JSONPlaceholder."""
    
    def __init__(self, client):
        self.client = client
        self.results: List[TestResult] = []
    
    def test_random_quote_200(self) -> TestResult:
        """Test 1: GET /posts/1 retourne HTTP 200 + JSON valide."""
        status, data, latency = self.client.get("/posts/1")
        
        passed = (status == 200 and 
                 isinstance(data, dict) and 
                 "title" in data and 
                 "body" in data)
        
        result = TestResult("GET /posts/1: HTTP 200 + valid JSON", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data, dict):
            result.details = "Not JSON"
        elif "title" not in data or "body" not in data:
            result.details = "Missing title/body"
        
        return result
    
    def test_quotes_list_endpoint(self) -> TestResult:
        """Test 2: GET /posts retourne liste."""
        status, data, latency = self.client.get("/posts", params={"_limit": 5})
        
        passed = (status == 200 and 
                 isinstance(data, list) and 
                 len(data) > 0)
        
        result = TestResult("GET /posts: returns list", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data, list):
            result.details = "Not a list"
        
        return result
    
    def test_authors_endpoint(self) -> TestResult:
        """Test 3: GET /users retourne liste d'utilisateurs."""
        status, data, latency = self.client.get("/users")
        
        passed = (status == 200 and 
                 isinstance(data, list) and 
                 len(data) > 0)
        
        result = TestResult("GET /users: returns users list", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data, list):
            result.details = "Not a list"
        
        return result
    
    def test_error_handling(self) -> TestResult:
        """Test 4: Gestion des erreurs (404 sur endpoint invalide)."""
        status, data, latency = self.client.get("/invalid-endpoint-xyz")
        
        passed = status == 404
        
        result = TestResult("Error handling: invalid endpoint returns 404", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 404:
            result.details = f"Expected 404, got {status}"
        
        return result
    
    def run_all(self) -> List[TestResult]:
        """Exécute tous les tests."""
        self.results = [
            self.test_random_quote_200(),
            self.test_quotes_list_endpoint(),
            self.test_authors_endpoint(),
            self.test_error_handling(),
        ]
        return self.results
