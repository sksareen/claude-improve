#!/bin/bash
# Start the complete Redis-powered real-time system

echo "🚀 Starting Redis-powered Claude system..."
echo ""

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis not running. Starting Redis..."
    if command -v brew > /dev/null; then
        brew services start redis
    else
        echo "Please start Redis manually: redis-server"
        exit 1
    fi
    sleep 2
fi

echo "✅ Redis is running"
echo ""

# Start components in background
echo "🌐 Starting Redis web server..."
cd web && python3 redis_watch.py &
WEB_PID=$!

echo "🤖 Starting Redis agent..."
python3 redis_agent.py &
AGENT_PID=$!

echo ""
echo "🎯 System started with TTI target: <50ms"
echo "📊 Web interface: http://localhost:3000"
echo "🔴 Redis PubSub: Active"
echo "🌐 WebSocket: ws://localhost:8765"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo ''; echo '🛑 Stopping all services...'; kill $WEB_PID $AGENT_PID; exit" INT
wait