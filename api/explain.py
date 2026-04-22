import sqlite3
import json
from http.server import BaseHTTPRequestHandler
import os

def get_scheme_from_db(scheme_name):
    """Query SQLite database for scheme details"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'schemes.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM schemes 
            WHERE LOWER(name) LIKE LOWER(?)
            LIMIT 1
        """, (f'%{scheme_name}%',))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_scheme_from_json(scheme_name):
    """Fallback to JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'schemes.json')
        with open(json_path, 'r') as f:
            schemes = json.load(f)
        
        for scheme in schemes:
            if scheme_name.lower() in scheme['name'].lower():
                return scheme
        return None
    except Exception as e:
        print(f"JSON error: {e}")
        return None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/explain':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            scheme_name = data.get('schemeName', '')
            
            if not scheme_name:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Scheme name required'}).encode())
                return
            
            scheme = get_scheme_from_db(scheme_name) or get_scheme_from_json(scheme_name)
            
            if scheme:
                response = {
                    'summary': scheme.get('description', 'No description available'),
                    'eligibility': scheme.get('eligibility', 'Eligibility criteria not specified'),
                    'benefits': scheme.get('benefits', 'Benefits information not available'),
                    'process': scheme.get('steps', 'Application process not specified')
                }
            else:
                response = {
                    'summary': f'{scheme_name} is a government initiative. Detailed information is being updated.',
                    'eligibility': 'Please check the official government portal for eligibility criteria.',
                    'benefits': 'Benefits vary based on the scheme. Visit the official website for details.',
                    'process': 'Apply through the official government portal or nearest Common Service Center.'
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
