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
    """Tests pour l'API Quotable."""
    
    def __init__(self, client):
        self.client = client
        self.results: List[TestResult] = []
    
    def test_random_quote_200(self) -> TestResult:
        """Test 1: GET /random retourne HTTP 200 + JSON valide."""
        status, data, latency = self.client.get("/random")
        
        passed = (status == 200 and 
                 isinstance(data, dict) and 
                 "content" in data and 
                 "author" in data)
        
        result = TestResult("GET /random: HTTP 200 + valid JSON", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data, dict):
            result.details = "Not JSON"
        elif "content" not in data or "author" not in data:
            result.details = "Missing content/author"
        
        return result
    
    def test_quotes_list_endpoint(self) -> TestResult:
        """Test 2: GET /quotes retourne liste."""
        status, data, latency = self.client.get("/quotes", params={"limit": 5})
        
        passed = (status == 200 and 
                 "results" in data and 
                 isinstance(data["results"], list) and 
                 len(data["results"]) > 0)
        
        result = TestResult("GET /quotes: returns results list", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data.get("results"), list):
            result.details = "No results array"
        
        return result
    
    def test_authors_endpoint(self) -> TestResult:
        """Test 3: GET /authors retourne liste d'auteurs."""
        status, data, latency = self.client.get("/authors")
        
        passed = (status == 200 and 
                 "results" in data and 
                 isinstance(data["results"], list) and 
                 len(data["results"]) > 0)
        
        result = TestResult("GET /authors: returns authors list", 
                           "PASS" if passed else "FAIL", 
                           latency)
        
        if status != 200:
            result.details = f"HTTP {status}"
        elif not isinstance(data.get("results"), list):
            result.details = "No results array"
        
        return result
    
    def test_error_handling(self) -> TestResult:
        """Test 4: Gestion des erreurs (404 sur endpoint invalide)."""
        status, data, latency = self.client.get("/invalid-endpoint")
        
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
