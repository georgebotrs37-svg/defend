from flask import Flask, request, abort, jsonify, make_response
import logging
from datetime import datetime
import urllib.parse
import re

app = Flask(__name__)

# إعداد Logging آمن وبسيط
logging.basicConfig(
    filename='403_bypass_attempts.log',
    level=logging.WARNING,
    format='%(asctime)s | %(message)s',
    encoding='utf-8',
    filemode='a'  # append mode
)

# Headers الشائعة في أدوات الـ 403 bypass
BYPASS_HEADERS = [
    'X-Forwarded-For', 'X-Forwarded-Host', 'X-Forwarded-Server',
    'X-Original-URL', 'X-Rewrite-URL', 'X-Client-IP', 'Client-IP',
    'X-Remote-Addr', 'X-Proxy', 'Forwarded', 'X-Host'
]

ALLOWED_METHODS = {'GET', 'POST', 'HEAD', 'OPTIONS'}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']

def is_path_suspicious(path):
    decoded = path
    for _ in range(6):
        prev = decoded
        decoded = urllib.parse.unquote(decoded)
        if decoded == prev:
            break
    
    lower_decoded = decoded.lower()
    suspicious = [
        r'\.\.', r'//', r'/\./', r'\\', r'%2e', r'%2f', r'%5c',
        r';', r'\.\.%00', r'..;/', r'0x', r'\x'
    ]
    if any(re.search(pat, lower_decoded) for pat in suspicious):
        return True
    
    if len(decoded) > 400 or '..' in decoded.split('/')[-1]:
        return True
    return False

@app.before_request
def security_shield():
    if not request.path.startswith('/protected'):
        return

    client_ip = request.remote_addr or 'unknown'
    host = request.headers.get('Host', 'unknown').lower()
    method = request.method
    full_path = request.path
    reason = ""

    if host not in ALLOWED_HOSTS:
        reason = f"Invalid Host: {host}"
        logging.warning(f"IP: {client_ip} | Method: {method} | Path: {full_path} | Host: {host} | Reason: {reason}")
        abort(403, "Invalid Host")

    if method not in ALLOWED_METHODS:
        reason = f"Blocked Method: {method}"
        logging.warning(f"IP: {client_ip} | Method: {method} | Path: {full_path} | Host: {host} | Reason: {reason}")
        resp = make_response("Nothing here 😴", 200)
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    detected_headers = [h for h in BYPASS_HEADERS if h in request.headers]
    if detected_headers:
        values = {h: request.headers.get(h) for h in detected_headers}
        reason = f"Suspicious headers: {values}"
        logging.warning(f"IP: {client_ip} | Method: {method} | Path: {full_path} | Host: {host} | Reason: {reason}")

    if is_path_suspicious(full_path):
        reason = "Path manipulation detected"
        logging.warning(f"IP: {client_ip} | Method: {method} | Path: {full_path} | Host: {host} | Reason: {reason}")
        abort(403, "Suspicious path")

    return None

@app.route('/protected/admin', methods=['GET', 'POST'])
def protected_admin():
    return jsonify({
        "status": "success",
        "message": "المنطقة محمية 🛡️",
        "time": datetime.now().isoformat(),
        "ip": request.remote_addr
    })

@app.route('/logs', methods=['GET'])
def show_logs():
    try:
        with open('403_bypass_attempts.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()[-50:]
        cleaned = [line.strip() for line in lines if line.strip()]
        return jsonify({"recent_attempts": cleaned})
    except FileNotFoundError:
        return jsonify({"error": "No log file yet"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("🛡️ Defense script is running!")
    print("Protected: /protected/*")
    print("Logs: 403_bypass_attempts.log")
    print("Check logs: http://127.0.0.1:5000/logs")
    app.run(host='127.0.0.1', port=5000, debug=False)