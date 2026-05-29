import requests
base='http://127.0.0.1:8080'
print('health', requests.get(base+'/health').status_code)
print('/mcp/tools', requests.get(base+'/mcp/tools').status_code)
print('/mcp/resources', requests.get(base+'/mcp/resources').status_code)
print('/mcp/prompts', requests.get(base+'/mcp/prompts').status_code)
print('/api/search_courses', requests.post(base+'/api/search_courses', json={'query':'Introduction'}).status_code)
print('/api/get_prerequisites', requests.post(base+'/api/get_prerequisites', json={'course_code':'CS102'}).status_code)
print('/api/lookup_instructor', requests.post(base+'/api/lookup_instructor', json={'instructor_name':'Alice Smith'}).status_code)
print('/api/get_prerequisite_graph', requests.post(base+'/api/get_prerequisite_graph', json={'course_code':'CS301'}).status_code)
