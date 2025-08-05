import os
import socket
import threading
import psutil
import logging
from flask import Flask, request, render_template_string
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from datetime import datetime
from werkzeug.serving import make_server

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_ip():
    for iface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family.name == 'AF_INET' and not snic.address.startswith("127."):
                ip = snic.address
                if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172."):
                    return ip
    return "127.0.0.1"

HTML = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Upload</title>
    <style>
      body { font-family: sans-serif; background: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; }
      .container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 0 15px #ccc; width: 90%%; max-width: 500px; }
      input[type="file"], textarea {
        font-size: 20px;
        padding: 12px;
        margin-top: 15px;
        width: 100%%;
        box-sizing: border-box;
      }
      textarea { height: 200px; resize: vertical; }

      input[type="submit"] {
        font-size: 22px;
        padding: 12px;
        margin-top: 15px;
        width: 100%%;
        border: none;
        border-radius: 6px;
        color: white;
        cursor: pointer;
      }
      input[name="submit_file"] { background-color: #007bff; }
      input[name="submit_text"] { background-color: #28a745; }
    </style>
  </head>
  <body>
    <div class="container">
      <h2>📤 Upload File</h2>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" name="submit_file" value="Upload File">
      </form>
      <h2>📝 Paste Text</h2>
      <form method="post">
        <textarea name="text" placeholder="Paste your text here..."></textarea>
        <input type="submit" name="submit_text" value="Upload Text">
      </form>
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'submit_file' in request.form:
            f = request.files['file']
            if f and f.filename:
                f.save(os.path.join(UPLOAD_FOLDER, f.filename))
                return '✅ File uploaded successfully. <a href="/">Go back</a>'
        elif 'submit_text' in request.form:
            text = request.form.get('text', '')
            if text.strip():
                filename = f"text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(os.path.join(UPLOAD_FOLDER, filename), 'w', encoding='utf-8') as f:
                    f.write(text)
                return '✅ Text saved successfully. <a href="/">Go back</a>'
    return render_template_string(HTML)

def run_flask(ip):
    # 关闭 Flask 控制台日志
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server = make_server(ip, 8001, app)
    server.serve_forever()

def run_http_server(ip):
    handler = SimpleHTTPRequestHandler
    with TCPServer((ip, 8080), handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    ip = get_ip()
    print(f"\n📥 Upload:   http://{ip}:8001")
    print(f"📤 Download: http://{ip}:8080\n")

    threading.Thread(target=run_flask, args=(ip,), daemon=True).start()
    run_http_server(ip)
