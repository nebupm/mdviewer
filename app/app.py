import os
import markdown
import re
from flask import Flask, render_template, abort, send_from_directory, request
from markupsafe import escape
import socket

app = Flask(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')

@app.route("/")
@app.route("/<path:foldername>")
def index(foldername=None):
    hostname = socket.gethostname()
    from_search = request.args.get('from_search')
    
    # Get list of folders in content directory
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
        
    folders = [d for d in os.listdir(CONTENT_DIR) if os.path.isdir(os.path.join(CONTENT_DIR, d))]
    folders.sort()
    
    path_parts = foldername.split('/') if foldername else []
    top_level_folder = path_parts[0] if path_parts else None
    folder_title = path_parts[-1] if path_parts else ""
    
    active_nav_items = []
    content_html = ""
    is_toc = False
    toc_items = []
    
    if foldername:
        folder_path = os.path.join(CONTENT_DIR, foldername)
        if not os.path.exists(folder_path):
            abort(404)
        
        # Build navigation items for the top-level folder in the sidebar
        top_level_path = os.path.join(CONTENT_DIR, top_level_folder)
        if os.path.exists(top_level_path):
            # Check if top-level folder has subdirectories
            top_subdirs = [d for d in os.listdir(top_level_path) if os.path.isdir(os.path.join(top_level_path, d)) and d != 'images']
            if top_subdirs:
                top_subdirs.sort()
                for subdir in top_subdirs:
                    rel_url_path = f"{top_level_folder}/{subdir}"
                    is_active = (len(path_parts) > 1 and path_parts[1] == subdir)
                    active_nav_items.append({
                        'label': subdir,
                        'path': rel_url_path,
                        'is_dir': True,
                        'is_active': is_active
                    })
            else:
                # Flat folder: list individual markdown files
                files = [f for f in os.listdir(top_level_path) if f.endswith('.md')]
                files.sort()
                for f in files:
                    file_rel_path = os.path.join(top_level_folder, f)
                    file_id = file_rel_path.replace('/', '-').replace('.', '-').replace(' ', '-')
                    label = os.path.splitext(f)[0]
                    active_nav_items.append({
                        'label': label,
                        'anchor': file_id,
                        'is_dir': False,
                        'is_active': False
                    })
        
        # Check if the requested folder itself has subdirectories (and thus needs a TOC)
        subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d)) and d != 'images']
        if subdirs:
            is_toc = True
            subdirs.sort()
            for subdir in subdirs:
                subdir_rel_path = os.path.join(foldername, subdir)
                toc_items.append({
                    'label': subdir,
                    'path': subdir_rel_path
                })
        else:
            # Walk through the folder_path recursively to find all markdown files
            grouped_files = {}
            for root, dirs, files in os.walk(folder_path):
                dirs.sort()
                files.sort()
                
                # Determine subdirectory path relative to folder_path
                rel_dir = os.path.relpath(root, folder_path)
                if rel_dir == '.':
                    rel_dir = ''
                
                md_in_dir = [f for f in files if f.endswith('.md')]
                if md_in_dir:
                    grouped_files[rel_dir] = md_in_dir
            
            html_parts = []
            for subdir in sorted(grouped_files.keys()):
                if subdir:
                    display_subdir = subdir.replace('/', ' ➔ ')
                    subdir_id = f"subdir-{foldername}-{subdir}".replace('/', '-').replace('.', '-').replace(' ', '-')
                    html_parts.append(f'<h2 id="{subdir_id}" class="subdir-header">📁 {display_subdir}</h2>')
                
                for md_file in grouped_files[subdir]:
                    if subdir:
                        file_rel_path = os.path.join(foldername, subdir, md_file)
                    else:
                        file_rel_path = os.path.join(foldername, md_file)
                    
                    filepath = os.path.join(CONTENT_DIR, file_rel_path)
                    subfolder_relpath = os.path.dirname(file_rel_path)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                        
                        # Rewrite image paths
                        text = re.sub(r'src="images/(.*?)"', rf'src="/content-images/{subfolder_relpath}/\1"', text)
                        text = re.sub(r'\(images/(.*?)\)', rf'(/content-images/{subfolder_relpath}/\1)', text)
                        
                        # Add an anchor for each file
                        file_id = file_rel_path.replace('/', '-').replace('.', '-').replace(' ', '-')
                        html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])
                        html_parts.append(f'<div id="{file_id}">{html_content}</div>')
            
            content_html = "<hr>".join(html_parts)
    
    return render_template('index.html', 
                           hostname=hostname, 
                           folders=folders, 
                           content=content_html,
                           active_folder=foldername,
                           top_level_folder=top_level_folder,
                           active_nav_items=active_nav_items,
                           is_toc=is_toc,
                           toc_items=toc_items,
                           folder_title=folder_title,
                           search_results=None,
                           search_query=None,
                           from_search=from_search)

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
            
            # Walk through folder_path recursively to find all markdown files
            for root, dirs, files in os.walk(folder_path):
                dirs.sort()
                files.sort()
                for md_file in files:
                    if md_file.endswith('.md'):
                        filepath = os.path.join(root, md_file)
                        rel_path = os.path.relpath(filepath, CONTENT_DIR)
                        
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
                                    
                                    # Format the relative file path under folder for display
                                    rel_path_under_folder = os.path.relpath(filepath, folder_path)
                                    display_file_name = rel_path_under_folder.replace('/', ' / ')
                                    
                                    file_id = rel_path.replace('/', '-').replace('.', '-').replace(' ', '-')
                                    
                                    # Get the relative path of the parent directory under CONTENT_DIR
                                    subfolder_path = os.path.relpath(root, CONTENT_DIR)
                                    
                                    results.append({
                                        'folder': folder,
                                        'subfolder_path': subfolder_path,
                                        'file': display_file_name,
                                        'file_id': file_id,
                                        'snippet': "..." + highlighted_snippet + "..."
                                    })
                        except Exception as e:
                            print(f"Error reading {filepath}: {e}")

    return render_template('index.html',
                           hostname=hostname,
                           folders=folders,
                           top_level_folder=None,
                           active_nav_items=None,
                           is_toc=False,
                           toc_items=None,
                           folder_title=None,
                           search_results=results,
                           search_query=query,
                           match_count=len(unique_folders_with_matches))

@app.route("/content-images/<path:subfolder_relpath>/<filename>")
def content_images(subfolder_relpath, filename):
    image_path = os.path.join(CONTENT_DIR, subfolder_relpath, 'images')
    return send_from_directory(image_path, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
