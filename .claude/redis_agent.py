#!/usr/bin/env python3
"""
Redis-powered Claude Agent - Sub-50ms TTI for feedback processing

Uses Redis PubSub for instant event-driven feedback processing
"""

import json
import time
import asyncio
import redis.asyncio as redis
from datetime import datetime
from pathlib import Path
import websockets
import threading


class RedisClaudeAgent:
    def __init__(self, claude_dir, redis_url="redis://localhost:6379"):
        self.claude_dir = Path(claude_dir)
        self.redis_url = redis_url
        self.redis_client = None
        self.pubsub = None
        self.websocket_clients = set()
        
        # Performance tracking
        self.tti_metrics = []
        
    async def start(self):
        """Start the Redis agent with PubSub"""
        self.redis_client = redis.from_url(self.redis_url)
        self.pubsub = self.redis_client.pubsub()
        
        # Subscribe to feedback channel
        await self.pubsub.subscribe("claude:feedback", "claude:context_update")
        
        print("🚀 Redis Claude Agent started")
        print(f"📊 Target TTI: <50ms")
        print(f"🔴 Redis: {self.redis_url}")
        print("⚡ PubSub mode - instant processing\n")
        
        # Start WebSocket server for real-time updates
        asyncio.create_task(self.start_websocket_server())
        
        # Start listening for messages
        await self.listen_for_feedback()
    
    async def start_websocket_server(self):
        """Start WebSocket server for real-time browser updates"""
        async def handle_client(websocket, path):
            self.websocket_clients.add(websocket)
            try:
                await websocket.wait_closed()
            finally:
                self.websocket_clients.discard(websocket)
        
        start_server = websockets.serve(handle_client, "localhost", 8765)
        await start_server
        print("🌐 WebSocket server started on ws://localhost:8765")
    
    async def listen_for_feedback(self):
        """Listen for Redis PubSub messages"""
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                start_time = time.time()
                
                try:
                    data = json.loads(message['data'])
                    channel = message['channel'].decode('utf-8')
                    
                    if channel == "claude:feedback":
                        await self.process_feedback_event(data)
                    elif channel == "claude:context_update":
                        await self.process_context_update(data)
                    
                    # Calculate TTI
                    tti_ms = (time.time() - start_time) * 1000
                    self.tti_metrics.append(tti_ms)
                    
                    # Keep only last 100 measurements
                    if len(self.tti_metrics) > 100:
                        self.tti_metrics = self.tti_metrics[-100:]
                    
                    avg_tti = sum(self.tti_metrics) / len(self.tti_metrics)
                    
                    print(f"⚡ Processed in {tti_ms:.1f}ms (avg: {avg_tti:.1f}ms)")
                    
                    # Broadcast update to WebSocket clients
                    await self.broadcast_update({
                        "type": "processing_complete",
                        "tti_ms": tti_ms,
                        "avg_tti_ms": avg_tti,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
    
    async def process_feedback_event(self, feedback_data):
        """Process feedback with sub-50ms target"""
        feedback_content = feedback_data.get('note', '')
        timestamp = feedback_data.get('timestamp', datetime.now().isoformat())
        
        # Fast analysis using pre-compiled patterns
        actions = self.fast_analyze_feedback(feedback_content)
        
        # Execute actions concurrently
        tasks = []
        for action in actions:
            if action['type'] == 'update_preferences':
                tasks.append(self.fast_update_preferences(action['data']))
            elif action['type'] == 'add_insight':
                tasks.append(self.fast_add_insight(action['data']))
        
        if tasks:
            await asyncio.gather(*tasks)
        
        # Store in Redis for fast retrieval
        await self.redis_client.setex(
            f"feedback:{timestamp}", 
            3600,  # 1 hour TTL
            json.dumps(feedback_data)
        )
    
    def fast_analyze_feedback(self, feedback):
        """Optimized feedback analysis with pre-compiled patterns"""
        feedback_lower = feedback.lower()
        actions = []
        
        # Pre-compiled keyword sets for O(1) lookup
        ui_keywords = {'ui', 'design', 'look', 'appearance', 'visual', 'ux'}
        perf_keywords = {'slow', 'fast', 'performance', 'speed', 'lag'}
        issue_keywords = {'bug', 'issue', 'problem', 'broken', 'not working'}
        positive_keywords = {'good', 'great', 'works', 'like', 'love', 'perfect'}
        
        words = set(feedback_lower.split())
        
        if words & ui_keywords:
            actions.append({
                'type': 'update_preferences',
                'data': {'category': 'ui_design', 'preference': feedback}
            })
        
        if words & issue_keywords:
            actions.append({
                'type': 'add_insight',
                'data': {'category': 'areas_for_improvement', 'insight': feedback}
            })
        
        if words & positive_keywords:
            actions.append({
                'type': 'add_insight', 
                'data': {'category': 'successful_patterns', 'insight': feedback}
            })
        
        return actions
    
    async def fast_update_preferences(self, data):
        """Fast preference update using Redis"""
        key = f"preferences:{data['category']}"
        await self.redis_client.setex(key, 3600, data['preference'])
    
    async def fast_add_insight(self, data):
        """Fast insight addition using Redis lists"""
        key = f"insights:{data['category']}"
        await self.redis_client.lpush(key, data['insight'])
        await self.redis_client.ltrim(key, 0, 9)  # Keep only last 10
    
    async def broadcast_update(self, message):
        """Broadcast update to all WebSocket clients"""
        if self.websocket_clients:
            message_str = json.dumps(message)
            tasks = [client.send(message_str) for client in self.websocket_clients.copy()]
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def get_tti_stats(self):
        """Get current TTI statistics"""
        if not self.tti_metrics:
            return {"avg_tti_ms": 0, "min_tti_ms": 0, "max_tti_ms": 0}
        
        return {
            "avg_tti_ms": sum(self.tti_metrics) / len(self.tti_metrics),
            "min_tti_ms": min(self.tti_metrics),
            "max_tti_ms": max(self.tti_metrics),
            "sample_count": len(self.tti_metrics)
        }


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Redis Claude Agent - Real-time feedback processing')
    parser.add_argument('--path', type=str, default='.', help='Path to .claude directory')
    parser.add_argument('--redis', type=str, default='redis://localhost:6379', help='Redis URL')
    
    args = parser.parse_args()
    
    agent = RedisClaudeAgent(Path(args.path).resolve(), args.redis)
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        print("\n🛑 Redis Agent stopped")
    except redis.ConnectionError:
        print("❌ Redis connection failed. Start Redis server: brew install redis && brew services start redis")


if __name__ == '__main__':
    asyncio.run(main())