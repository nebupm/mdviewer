import os
import markdown
import re
from flask import Flask, render_template, abort, send_from_directory
import socket

app = Flask(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')

@app.route("/")
@app.route("/<foldername>")
def index(foldername=None):
    hostname = socket.gethostname()
    
    # Get list of folders in content directory
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
        
    folders = [d for d in os.listdir(CONTENT_DIR) if os.path.isdir(os.path.join(CONTENT_DIR, d))]
    folders.sort()
    
    content_html = ""
    if foldername:
        folder_path = os.path.join(CONTENT_DIR, foldername)
        if not os.path.exists(folder_path):
            abort(404)
        
        # Read all markdown files in the folder
        md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
        md_files.sort()
        
        html_parts = []
        for md_file in md_files:
            filepath = os.path.join(folder_path, md_file)
            with open(filepath, 'r') as f:
                text = f.read()
                # Simple regex to prefix image paths starting with images/
                text = re.sub(r'src="images/(.*?)"', rf'src="/content-images/{foldername}/\1"', text)
                text = re.sub(r'\(images/(.*?)\)', rf'(/content-images/{foldername}/\1)', text)
                
                html_parts.append(markdown.markdown(text, extensions=['tables', 'fenced_code']))
        
        content_html = "<hr>".join(html_parts)
    
    return render_template('index.html', 
                           hostname=hostname, 
                           folders=folders, 
                           content=content_html,
                           active_folder=foldername)

@app.route("/content-images/<foldername>/<filename>")
def content_images(foldername, filename):
    image_path = os.path.join(CONTENT_DIR, foldername, 'images')
    return send_from_directory(image_path, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
