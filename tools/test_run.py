from pathlib import Path
import sys
import subprocess
import time
import requests
import json

# Ensure project root is on sys.path so 'src' package imports work when this
# script is executed directly.
proj_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

from data.seed_script.seed import seed_database

# Seed the DB (idempotent)
seed_database(str(proj_root / 'data' / 'catalog.db'))

uvicorn_cmd = [sys.executable, '-m', 'uvicorn', 'src.main:app', '--host', '127.0.0.1', '--port', '8080']
print('Starting uvicorn...')
proc = subprocess.Popen(uvicorn_cmd, cwd=str(proj_root))

try:
	# Wait for server to become healthy
	base = 'http://127.0.0.1:8080'
	for i in range(30):
		try:
			r = requests.get(base + '/health', timeout=1)
			if r.status_code == 200:
				print('Server healthy')
				break
		except requests.RequestException:
			pass
		time.sleep(0.5)
	else:
		raise RuntimeError('Server did not become healthy in time')

	def show(path, method='get', json_payload=None):
		url = base + path
		if method == 'get':
			r = requests.get(url)
		else:
			r = requests.post(url, json=json_payload)
		print(f'\n{method.upper()} {path} ->', r.status_code)
		try:
			print(json.dumps(r.json(), indent=2))
		except Exception:
			print(r.text)

	show('/health')
	show('/mcp/tools')
	show('/mcp/resources')
	show('/mcp/prompts')

	show('/api/search_courses', method='post', json_payload={'query': 'Introduction'})
	show('/api/get_prerequisites', method='post', json_payload={'course_code': 'CS102'})
	show('/api/lookup_instructor', method='post', json_payload={'instructor_name': 'Alice Smith'})
	show('/api/get_prerequisite_graph', method='post', json_payload={'course_code': 'CS301'})

finally:
	print('Stopping uvicorn...')
	proc.terminate()
	try:
		proc.wait(timeout=5)
	except Exception:
		proc.kill()
