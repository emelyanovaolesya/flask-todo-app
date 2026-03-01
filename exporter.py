from flask import Flask
import requests
import time

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    endpoints = [
        ('GET', '/', None),
        ('POST', '/add', {'todo_item': 'test'}),
        ('POST', '/update', {'todo_item': 'update'})
    ]
    
    ts = int(time.time())
    requests_data = []
    duration_data = []
    
    for method, path, data in endpoints:
        start = time.time()
        try:
            if data:
                resp = requests.request(method, f'http://localhost:5000{path}', 
                                      data=data, timeout=3, allow_redirects=False)
            else:
                resp = requests.request(method, f'http://localhost:5000{path}', 
                                      timeout=3, allow_redirects=False)
            
            duration = time.time() - start
            requests_data.append((method, path, resp.status_code))
            duration_data.append((method, path, resp.status_code, duration))
            
        except Exception as e:
            duration = time.time() - start
            requests_data.append((method, path, 'ERROR'))
            duration_data.append((method, path, 'ERROR', duration))

    lines = [
        '# HELP todo_endpoint_available Endpoint availability',
        '# TYPE todo_endpoint_available gauge',
    ]
    
    for method, path, status in requests_data:
        lines.append(f'todo_endpoint_available{{method="{method}",endpoint="{path}",status="{status}"}} 1 {ts}')
    
    lines.extend([
        '',
        '# HELP todo_request_duration_seconds HTTP request duration in seconds',
        '# TYPE todo_request_duration_seconds gauge',
    ])
    
    for method, path, status, duration in duration_data:
        lines.append(f'todo_request_duration_seconds{{method="{method}",endpoint="{path}",status="{status}"}} {duration:.3f} {ts}')
    
    return '\n'.join(lines), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    print('Todo Exporter: http://localhost:8000/metrics')
    app.run(host='0.0.0.0', port=8000, debug=False)
