#!/usr/bin/env python3
"""
Redis-powered web server with real-time TTI tracking

Publishes feedback events to Redis and receives real-time updates via WebSocket
"""

import json
import asyncio
import redis.asyncio as redis
import websockets
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time


class RedisWebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, redis_client=None, **kwargs):
        self.redis_client = redis_client
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Suppress default HTTP server logging"""
        return

    def do_GET(self):
        url_path = self.path.split('?')[0]

        if url_path == '/' or url_path == '/index.html':
            self.serve_html()
        elif url_path == '/api/context':
            self.serve_context_api()
        elif url_path == '/api/feedback':
            self.serve_feedback_api()
        elif url_path == '/api/tti':
            self.serve_tti_api()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/feedback':
            asyncio.run(self.handle_feedback_post())
        else:
            self.send_error(404)

    def serve_html(self):
        """Serve enhanced HTML with WebSocket connection and TTI metrics"""
        html_content = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Claude Context Viewer - Real-Time</title>
    <style>
        /* Existing styles... */
        .tti-metric {
            background: #00ff88;
            color: #1a1a1a;
            padding: 4px 8px;
            border-radius: 2px;
            font-weight: bold;
        }
        .tti-good { background: #00ff88; }
        .tti-warning { background: #ffaa00; }
        .tti-bad { background: #ff4444; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <div class="tab-indicator">Context (Tab)</div>
            <div class="stat-item">
                <span class="status-dot status-online"></span>
                Redis: <span class="stat-value" id="redis-status">Connecting...</span>
            </div>
            <div class="stat-item">
                TTI: <span class="tti-metric" id="tti-display">--ms</span>
            </div>
        </div>
        <div class="header-right">
            <div class="stat-item">
                Avg TTI: <span class="stat-value" id="avg-tti">--ms</span>
            </div>
            <div class="stat-item">
                Events: <span class="stat-value" id="event-count">0</span>
            </div>
            <div class="stat-item">
                Last Updated: <span class="stat-value" id="header-last-update">--</span>
            </div>
        </div>
    </div>

    <!-- Rest of your existing HTML structure -->

    <script>
        // WebSocket connection for real-time updates
        let ws = null;
        let eventCount = 0;
        let lastTTI = 0;

        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8765');

            ws.onopen = function() {
                document.getElementById('redis-status').textContent = 'Connected';
                console.log('WebSocket connected');
            };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);

                if (data.type === 'processing_complete') {
                    updateTTIMetrics(data.tti_ms, data.avg_tti_ms);
                    eventCount++;
                    document.getElementById('event-count').textContent = eventCount;
                }
            };

            ws.onclose = function() {
                document.getElementById('redis-status').textContent = 'Disconnected';
                setTimeout(connectWebSocket, 1000); // Reconnect
            };
        }

        function updateTTIMetrics(tti, avgTTI) {
            const ttiDisplay = document.getElementById('tti-display');
            const avgTTIDisplay = document.getElementById('avg-tti');

            ttiDisplay.textContent = `${tti.toFixed(1)}ms`;
            avgTTIDisplay.textContent = `${avgTTI.toFixed(1)}ms`;

            // Color code TTI performance
            ttiDisplay.className = 'tti-metric ';
            if (tti < 50) ttiDisplay.className += 'tti-good';
            else if (tti < 200) ttiDisplay.className += 'tti-warning';
            else ttiDisplay.className += 'tti-bad';

            lastTTI = tti;
        }

        async function addQuickFeedback() {
            const note = document.getElementById('quick-note').value.trim();
            if (!note) return;

            const startTime = performance.now();

            try {
                await fetch('/api/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        type: 'quick_note',
                        category: 'user_input',
                        note: note,
                        timestamp: new Date().toISOString(),
                        client_timestamp: startTime
                    })
                });

                document.getElementById('quick-note').value = '';
            } catch (error) {
                console.error('Error adding feedback:', error);
            }
        }

        // Connect WebSocket on load
        connectWebSocket();

        // Rest of your existing JavaScript...
    </script>
</body>
</html>'''

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    async def handle_feedback_post(self):
        """Publish feedback to Redis PubSub for instant processing"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            feedback_data = json.loads(post_data.decode('utf-8'))

            # Add server timestamp for TTI calculation
            feedback_data['server_timestamp'] = time.time()

            # Publish to Redis for instant processing
            await self.redis_client.publish(
                'claude:feedback',
                json.dumps(feedback_data)
            )

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "published",
                "message": "Feedback sent to Redis for instant processing"
            }).encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Error publishing feedback: {e}")

    def serve_tti_api(self):
        """Serve TTI metrics"""
        # This would connect to Redis to get real TTI stats
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "current_tti_ms": 0,
            "avg_tti_ms": 0,
            "target_tti_ms": 50
        }).encode('utf-8'))


async def start_redis_server(port=3000, redis_url="redis://localhost:6379"):
    """Start the Redis-powered web server"""
    redis_client = redis.from_url(redis_url)

    def create_handler(*args, **kwargs):
        return RedisWebHandler(*args, redis_client=redis_client, **kwargs)

    server = HTTPServer(('localhost', port), create_handler)

    print(f"🚀 Redis Web Server starting on http://localhost:{port}")
    print(f"🔴 Redis: {redis_url}")
    print(f"📊 TTI Target: <50ms")
    print(f"🌐 WebSocket: ws://localhost:8765")

    # Run server in thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return server


if __name__ == '__main__':
    asyncio.run(start_redis_server())
