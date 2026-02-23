from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"🌆 Twilight Net running at http://localhost:{PORT}")
HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler).serve_forever()
