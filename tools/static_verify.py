import os, sys, json
from pathlib import Path
import sqlite3

root = Path.cwd()
print('Repo root:', root)

checks = {}

# Required files
required = ['docker-compose.yml','Dockerfile','.env.example','data/catalog.db','data/seed_script/seed.py','prompts/course_comparison_template.txt','README.md']
for r in required:
    checks[r] = (root / r).exists()

# DB schema and counts
db = root / 'data' / 'catalog.db'
if db.exists():
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    tables = {}
    for t in ['departments','instructors','courses','prerequisites']:
        try:
            cur.execute(f"SELECT count(*) FROM {t}")
            tables[t] = cur.fetchone()[0]
        except Exception as e:
            tables[t] = str(e)
    conn.close()
else:
    tables = {t: 'missing' for t in ['departments','instructors','courses','prerequisites']}

# OpenAPI paths (import app)
sys.path.insert(0, str(root))
openapi_ok = False
paths = []
try:
    from src.main import app
    spec = app.openapi()
    paths = list(spec.get('paths', {}).keys())
    openapi_ok = any(p.startswith('/api') for p in paths) and '/mcp/tools' in paths
except Exception as e:
    paths = [str(e)]

report = {
    'files': checks,
    'tables': tables,
    'openapi_paths_sample': paths[:20],
    'openapi_ok': openapi_ok
}

print(json.dumps(report, indent=2))

# Determine pass/fail
requirements = {
    'departments': 3,
    'instructors': 5,
    'courses': 10,
    'prerequisites': 3
}

passed = all(checks.values()) and all(isinstance(tables[k], int) and tables[k]>=requirements[k] for k in requirements) and openapi_ok
print('\nFINAL PASS:', passed)
