"""
Storage: SQLite pour historique des runs.
"""
import sqlite3
import json
from typing import Dict, List, Any
from datetime import datetime
import os

class RunStorage:
    def __init__(self, db_path: str = "test_runs.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Crée la table si elle n'existe pas."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                summary TEXT NOT NULL,
                tests_json TEXT NOT NULL,
                passed INTEGER,
                failed INTEGER,
                error_rate REAL,
                latency_avg REAL,
                latency_p95 REAL
            )
        """)
        conn.commit()
        conn.close()
    
    def save_run(self, run_result: Dict[str, Any]) -> int:
        """
        Sauvegarde un run de test.
        
        Returns:
            ID de la run
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        summary = run_result.get("summary", {})
        
        cursor.execute("""
            INSERT INTO test_runs 
            (api, timestamp, summary, tests_json, passed, failed, error_rate, latency_avg, latency_p95)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_result.get("api"),
            run_result.get("timestamp"),
            json.dumps(summary),
            json.dumps(run_result.get("tests", [])),
            summary.get("passed", 0),
            summary.get("failed", 0),
            summary.get("error_rate", 0),
            summary.get("latency_ms_avg", 0),
            summary.get("latency_ms_p95", 0)
        ))
        
        conn.commit()
        run_id = cursor.lastrowid
        conn.close()
        
        return run_id
    
    def get_last_run(self) -> Dict[str, Any]:
        """Récupère le dernier run."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, api, timestamp, summary, tests_json, passed, failed, error_rate, latency_avg, latency_p95
            FROM test_runs
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "api": row[1],
            "timestamp": row[2],
            "summary": json.loads(row[3]),
            "tests": json.loads(row[4]),
            "passed": row[5],
            "failed": row[6],
            "error_rate": row[7],
            "latency_avg": row[8],
            "latency_p95": row[9]
        }
    
    def list_runs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Liste les derniers runs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, api, timestamp, summary, tests_json, passed, failed, error_rate, latency_avg, latency_p95
            FROM test_runs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        runs = []
        for row in rows:
            runs.append({
                "id": row[0],
                "api": row[1],
                "timestamp": row[2],
                "summary": json.loads(row[3]),
                "tests": json.loads(row[4]),
                "passed": row[5],
                "failed": row[6],
                "error_rate": row[7],
                "latency_avg": row[8],
                "latency_p95": row[9]
            })
        
        return runs
    
    def get_stats(self) -> Dict[str, Any]:
        """Calcule les stats globales."""
        runs = self.list_runs(limit=100)
        
        if not runs:
            return {
                "total_runs": 0,
                "avg_error_rate": 0,
                "avg_latency": 0,
                "last_run": None
            }
        
        avg_error_rate = sum(r["error_rate"] for r in runs) / len(runs) if runs else 0
        avg_latency = sum(r["latency_avg"] for r in runs) / len(runs) if runs else 0
        
        return {
            "total_runs": len(runs),
            "avg_error_rate": round(avg_error_rate, 3),
            "avg_latency": round(avg_latency, 2),
            "last_run": runs[0] if runs else None
        }
