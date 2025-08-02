#!/bin/bash
# Start Claude Agent to process feedback autonomously

echo "🤖 Starting Claude Agent..."
echo "📁 Working directory: $(pwd)"
echo ""

# Start the agent in the current directory
python3 claude_agent.py --path .

echo ""
echo "🛑 Claude Agent stopped"