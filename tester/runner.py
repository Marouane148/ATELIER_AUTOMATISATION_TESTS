"""
Runner : orchestration des tests + calcul des métriques QoS.
"""
from datetime import datetime, timezone
from typing import Dict, List, Any
from .client import APIClient
from .tests import QuotableTests, TestResult
import statistics

class TestRunner:
    def __init__(self, api_base_url: str = "https://jsonplaceholder.typicode.com"):
        self.api_base_url = api_base_url
        self.client = APIClient(api_base_url, timeout=5)
    
    def run(self) -> Dict[str, Any]:
        """
        Exécute tous les tests et retourne un résumé avec métriques QoS.
        
        Returns:
            {
                "api": "Quotable",
                "timestamp": "2026-03-04T...",
                "summary": {
                    "passed": int,
                    "failed": int,
                    "error_rate": float,
                    "latency_ms_avg": float,
                    "latency_ms_p95": float
                },
                "tests": [...]
            }
        """
        tester = QuotableTests(self.client)
        results = tester.run_all()
        
        # Calcul des métriques
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status != "PASS")
        total = len(results)
        error_rate = failed / total if total > 0 else 0
        
        latencies = [r.latency_ms for r in results if r.latency_ms > 0]
        latency_avg = statistics.mean(latencies) if latencies else 0
        latency_p95 = self._percentile(latencies, 95) if latencies else 0
        
        return {
            "api": "Quotable",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "passed": passed,
                "failed": failed,
                "error_rate": round(error_rate, 3),
                "latency_ms_avg": round(latency_avg, 2),
                "latency_ms_p95": round(latency_p95, 2)
            },
            "tests": [r.to_dict() for r in results]
        }
    
    @staticmethod
    def _percentile(data: List[float], percentile: int) -> float:
        """Calcule le percentile d'une liste."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
