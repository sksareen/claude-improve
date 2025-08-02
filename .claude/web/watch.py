#!/usr/bin/env python3
"""
Claude Context Viewer - File watcher with web interface

This script watches the .claude directory for changes and serves a real-time
web interface showing current context, feedback, and performance metrics.

Usage:
    python3 watch.py [--port 3000]
"""

import json
import os
import sys
import time
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse, parse_qs
import argparse


class ClaudeContextHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, base_path=None, **kwargs):
        self.base_path = base_path or Path(__file__).parent.parent
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Suppress default HTTP server logging"""
        return

    def do_GET(self):
        url_path = urlparse(self.path).path
        
        if url_path == '/' or url_path == '/index.html':
            self.serve_html()
        elif url_path == '/api/context':
            self.serve_context_api()
        elif url_path == '/api/feedback':
            self.serve_feedback_api()
        elif url_path == '/api/ux_config':
            self.serve_ux_config()
        else:
            self.send_error(404)

    def do_POST(self):
        url_path = urlparse(self.path).path
        
        if url_path == '/api/feedback':
            self.handle_feedback_post()
        else:
            self.send_error(404)

    def serve_html(self):
        """Serve the main HTML interface"""
        try:
            html_path = self.base_path / 'web' / 'index.html'
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error serving HTML: {e}")

    def serve_context_api(self):
        """Serve current context data as JSON"""
        try:
            context_path = self.base_path / 'context.json'
            
            if context_path.exists():
                with open(context_path, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
            else:
                context_data = {
                    "current_context": {
                        "active_focus": "Context file not found",
                        "progress_status": "unknown",
                        "next_priority": "Create context.json"
                    },
                    "todo_status": {
                        "completed": 0,
                        "in_progress": 0,
                        "pending": 0
                    }
                }

            self.send_json_response(context_data)
        except Exception as e:
            self.send_error(500, f"Error loading context: {e}")

    def serve_feedback_api(self):
        """Serve feedback data as JSON"""
        try:
            feedback_path = self.base_path / 'feedback.json'
            
            if feedback_path.exists():
                with open(feedback_path, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
            else:
                feedback_data = {
                    "feedback_log": [],
                    "performance_notes": {
                        "fast_patterns": [],
                        "slow_patterns": []
                    },
                    "insights": {
                        "successful_patterns": [],
                        "areas_for_improvement": []
                    }
                }

            self.send_json_response(feedback_data)
        except Exception as e:
            self.send_error(500, f"Error loading feedback: {e}")

    def handle_feedback_post(self):
        """Handle POST request to add new feedback"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_feedback = json.loads(post_data.decode('utf-8'))
            
            feedback_path = self.base_path / 'feedback.json'
            
            # Load existing feedback
            if feedback_path.exists():
                with open(feedback_path, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
            else:
                feedback_data = {"feedback_log": []}
            
            # Add new feedback
            if 'feedback_log' not in feedback_data:
                feedback_data['feedback_log'] = []
            
            feedback_data['feedback_log'].append(new_feedback)
            
            # Keep only last 50 feedback items
            if len(feedback_data['feedback_log']) > 50:
                feedback_data['feedback_log'] = feedback_data['feedback_log'][-50:]
            
            # Update last_updated
            if 'project_meta' in feedback_data:
                feedback_data['project_meta']['last_updated'] = datetime.now().isoformat() + 'Z'
            
            # Save back to file
            with open(feedback_path, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2, ensure_ascii=False)
            
            # Create identity query file for Claude to pick up
            identity_query_path = self.base_path / 'identity_query.json'
            identity_query = {
                "timestamp": datetime.now().isoformat() + 'Z',
                "trigger": "feedback_submitted",
                "feedback_content": new_feedback['note'],
                "query_type": "identity_update",
                "status": "pending",
                "context": "User submitted feedback that should be processed by Claude"
            }
            
            with open(identity_query_path, 'w', encoding='utf-8') as f:
                json.dump(identity_query, f, indent=2, ensure_ascii=False)
            
            # Process UX changes immediately
            self.process_ux_feedback(new_feedback['note'])
            
            self.send_json_response({
                "status": "success", 
                "message": "Feedback added and identity query created"
            })
        except Exception as e:
            self.send_error(500, f"Error adding feedback: {e}")

    def process_ux_feedback(self, feedback_content):
        """Process UX feedback and generate CSS changes"""
        feedback_lower = feedback_content.lower()
        css_updates = {}
        
        # Zen/calm color scheme
        if any(word in feedback_lower for word in ['zen', 'calm', 'peaceful', 'soothing']):
            css_updates.update({
                'zen_mode': True,
                'background_color': '#0a0f0a',
                'panel_color': '#1a251a', 
                'text_color': '#d0e0d0',
                'accent_color': '#6b9a6b',
                'border_color': '#2a4a2a'
            })
        
        # Dark mode enhancements
        if any(word in feedback_lower for word in ['dark', 'darker', 'black']):
            css_updates.update({
                'dark_mode': True,
                'background_color': '#000000',
                'panel_color': '#111111',
                'text_color': '#ffffff'
            })
        
        # Settings button request
        if any(word in feedback_lower for word in ['settings', 'customize', 'config']):
            css_updates['show_settings'] = True
        
        # TTI/uptime fixes
        if any(word in feedback_lower for word in ['tti', 'uptime', 'header']):
            css_updates['fix_header_metrics'] = True
        
        if css_updates:
            self.save_ux_config(css_updates)

    def serve_ux_config(self):
        """Serve UX configuration for dynamic theme changes"""
        try:
            config_path = self.base_path / 'ux_config.json'
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                # Default config
                config = {
                    'theme': 'default',
                    'colors': {},
                    'features': {},
                    'last_updated': None
                }
            
            self.send_json_response(config)
        except Exception as e:
            self.send_error(500, f"Error loading UX config: {e}")

    def save_ux_config(self, updates):
        """Save UX configuration that the frontend can pick up"""
        config_path = self.base_path / 'ux_config.json'
        
        try:
            # Load existing config
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {
                    'theme': 'default',
                    'colors': {},
                    'features': {},
                    'last_updated': None
                }
            
            # Apply updates
            for key, value in updates.items():
                if key.endswith('_color'):
                    config['colors'][key] = value
                elif key in ['zen_mode', 'dark_mode']:
                    config['theme'] = key
                elif key.startswith('show_') or key.startswith('fix_'):
                    config['features'][key] = value
                else:
                    config[key] = value
            
            config['last_updated'] = datetime.now().isoformat() + 'Z'
            
            # Save config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"🎨 UX config updated: {list(updates.keys())}")
        
        except Exception as e:
            print(f"❌ Error saving UX config: {e}")

    def send_json_response(self, data):
        """Send JSON response with proper headers"""
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))


class FileWatcher:
    """Watch .claude directory for changes and track modification times"""
    
    def __init__(self, watch_path):
        self.watch_path = Path(watch_path)
        self.file_times = {}
        self.update_file_times()
    
    def update_file_times(self):
        """Update the modification times for all watched files"""
        watch_files = [
            self.watch_path / 'context.json',
            self.watch_path / 'feedback.json',
            self.watch_path / 'memory.md'
        ]
        
        for file_path in watch_files:
            if file_path.exists():
                self.file_times[str(file_path)] = file_path.stat().st_mtime
    
    def check_for_changes(self):
        """Check if any watched files have been modified"""
        changes = []
        watch_files = [
            self.watch_path / 'context.json',
            self.watch_path / 'feedback.json',
            self.watch_path / 'memory.md'
        ]
        
        for file_path in watch_files:
            if file_path.exists():
                current_time = file_path.stat().st_mtime
                file_key = str(file_path)
                
                if file_key not in self.file_times or self.file_times[file_key] != current_time:
                    changes.append(file_path.name)
                    self.file_times[file_key] = current_time
        
        return changes


def create_handler_class(base_path):
    """Create handler class with base_path bound"""
    class BoundHandler(ClaudeContextHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, base_path=base_path, **kwargs)
    return BoundHandler


def start_server(port=3000, base_path=None):
    """Start the HTTP server"""
    if base_path is None:
        base_path = Path(__file__).parent.parent
    
    print(f"🧠 Claude Context Viewer starting...")
    print(f"📁 Watching: {base_path}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"⚡ Auto-refresh: 2 seconds")
    print(f"🔥 Press Ctrl+C to stop\n")
    
    handler_class = create_handler_class(base_path)
    server = HTTPServer(('localhost', port), handler_class)
    
    # Start file watcher in background thread
    watcher = FileWatcher(base_path)
    
    def watch_files():
        while True:
            try:
                changes = watcher.check_for_changes()
                if changes:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 📝 File changes detected: {', '.join(changes)}")
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"File watcher error: {e}")
    
    watcher_thread = Thread(target=watch_files, daemon=True)
    watcher_thread.start()
    
    # Auto-open browser
    def open_browser():
        time.sleep(1)  # Give server time to start
        webbrowser.open(f'http://localhost:{port}')
    
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description='Claude Context Viewer - Real-time feedback interface')
    parser.add_argument('--port', type=int, default=3000, help='Port to run server on (default: 3000)')
    parser.add_argument('--path', type=str, help='Path to .claude directory (default: auto-detect)')
    
    args = parser.parse_args()
    
    # Determine base path
    if args.path:
        base_path = Path(args.path)
    else:
        base_path = Path(__file__).parent.parent
    
    # Validate path
    if not base_path.exists():
        print(f"❌ Error: Directory {base_path} does not exist")
        sys.exit(1)
    
    # Check for required files
    context_file = base_path / 'context.json'
    feedback_file = base_path / 'feedback.json'
    
    if not context_file.exists() and not feedback_file.exists():
        print(f"⚠️  Warning: No context or feedback files found in {base_path}")
        print("   The viewer will still work but may show empty data.")
        print("   Make sure you're running from the correct directory.\n")
    
    try:
        start_server(args.port, base_path)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {args.port} is already in use.")
            print(f"   Try a different port: python3 watch.py --port {args.port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()