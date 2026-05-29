import requests
import json

base = 'http://127.0.0.1:8080'

checks = []

def check_get(path):
    url = base + path
    try:
        r = requests.get(url, timeout=3)
        return (path, r.status_code, r.json() if r.headers.get('Content-Type','').startswith('application/json') else r.text)
    except Exception as e:
        return (path, 'error', str(e))

def check_post(path, payload):
    url = base + path
    try:
        r = requests.post(url, json=payload, timeout=4)
        return (path, r.status_code, r.json())
    except Exception as e:
        return (path, 'error', str(e))

paths = [
    ('GET','/health', None),
    ('GET','/mcp/tools', None),
    ('GET','/mcp/resources', None),
    ('GET','/mcp/prompts', None),
    ('POST','/api/search_courses', {'query':'Introduction'}),
    ('POST','/api/get_prerequisites', {'course_code':'CS102'}),
    ('POST','/api/lookup_instructor', {'instructor_name':'Alice Smith'}),
    ('POST','/api/get_prerequisite_graph', {'course_code':'CS301'})
]

for method, path, payload in paths:
    if method=='GET':
        res = check_get(path)
    else:
        res = check_post(path, payload)
    print(json.dumps(res, indent=2))
