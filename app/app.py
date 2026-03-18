import os
import markdown
import re
from flask import Flask, render_template, abort, send_from_directory, request
from markupsafe import escape
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
                
                # Add an anchor for each file
                file_id = md_file.replace('.', '-').replace(' ', '-')
                html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])
                html_parts.append(f'<div id="{file_id}">{html_content}</div>')
        
        content_html = "<hr>".join(html_parts)
    
    return render_template('index.html', 
                           hostname=hostname, 
                           folders=folders, 
                           content=content_html,
                           active_folder=foldername,
                           search_results=None,
                           search_query=None)

@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    hostname = socket.gethostname()
    
    folders = [d for d in os.listdir(CONTENT_DIR) if os.path.isdir(os.path.join(CONTENT_DIR, d))]
    folders.sort()
    
    results = []
    unique_folders_with_matches = set()
    
    if query:
        for folder in folders:
            folder_path = os.path.join(CONTENT_DIR, folder)
            md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
            
            for md_file in md_files:
                filepath = os.path.join(folder_path, md_file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            unique_folders_with_matches.add(folder)
                            # Highlight the search term in the snippet
                            # Use a simple case-insensitive replace
                            start_index = content.lower().find(query.lower())
                            snippet_start = max(0, start_index - 50)
                            snippet_end = min(len(content), start_index + len(query) + 50)
                            snippet = content[snippet_start:snippet_end]
                            
                            # Escape for safety before adding HTML tags
                            escaped_snippet = str(escape(snippet))
                            
                            # Simple case-insensitive highlight
                            pattern = re.compile(re.escape(query), re.IGNORECASE)
                            highlighted_snippet = pattern.sub(lambda m: f'<mark>{m.group()}</mark>', escaped_snippet)
                            
                            results.append({
                                'folder': folder,
                                'file': md_file,
                                'file_id': md_file.replace('.', '-').replace(' ', '-'),
                                'snippet': "..." + highlighted_snippet + "..."
                            })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    return render_template('index.html',
                           hostname=hostname,
                           folders=folders,
                           search_results=results,
                           search_query=query,
                           match_count=len(unique_folders_with_matches))

@app.route("/content-images/<foldername>/<filename>")
def content_images(foldername, filename):
    image_path = os.path.join(CONTENT_DIR, foldername, 'images')
    return send_from_directory(image_path, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
