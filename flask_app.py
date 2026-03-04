from flask import Flask, render_template, jsonify, request
from tester.runner import TestRunner
from storage import RunStorage
import json

app = Flask(__name__)
storage = RunStorage("test_runs.db")

@app.get("/")
def consignes():
    return render_template('consignes.html')

@app.get("/run")
def run_tests():
    """Exécute les tests et sauvegarde les résultats."""
    try:
        runner = TestRunner("https://jsonplaceholder.typicode.com")
        result = runner.run()
        
        # Sauvegarde dans SQLite
        storage.save_run(result)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/dashboard")
def dashboard():
    """Page HTML du dashboard avec historique et dernier run."""
    return render_template('dashboard.html')

@app.get("/api/dashboard-data")
def dashboard_data():
    """API JSON pour alimenter le dashboard."""
    stats = storage.get_stats()
    return jsonify(stats), 200

@app.get("/api/runs")
def get_runs():
    """Liste les derniers runs en JSON."""
    limit = request.args.get('limit', 20, type=int)
    runs = storage.list_runs(limit=limit)
    return jsonify({"runs": runs}), 200

@app.get("/health")
def health():
    """Health check : retourne l'état de la dernière run."""
    last_run = storage.get_last_run()
    if not last_run:
        return jsonify({
            "status": "OK",
            "message": "Service running, no runs yet",
            "last_run": None
        }), 200
    
    health_status = "HEALTHY" if last_run["error_rate"] < 0.2 else "DEGRADED"
    
    return jsonify({
        "status": health_status,
        "last_run": last_run["timestamp"],
        "error_rate": last_run["error_rate"],
        "latency_avg_ms": last_run["latency_avg"],
        "passed": last_run["passed"],
        "failed": last_run["failed"]
    }), 200

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
