# Claude Improvement Project

A real-time feedback and context management system designed to make Claude more performant and helpful by maintaining structured memory across sessions.

## 🚀 Quick Start

### Option 1: Basic File-Based System
```bash
# Start the real-time viewer (no dependencies)
cd .claude/web && python3 watch.py

# In another terminal, start the Claude agent (optional)
cd .claude && ./start_agent.sh

# View at http://localhost:3000
```

### Option 2: High-Performance Redis System (TTI <50ms)
```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (macOS)
brew install redis && brew services start redis

# Start the complete system
cd .claude && ./start_redis_system.sh

# View at http://localhost:3000 with real-time WebSocket updates
```

## 📁 Project Structure

```
claude-improve/
├── CLAUDE.md                 # Main guidance for Claude
├── .claude/                  # Context management system
│   ├── feedback.json         # Real-time feedback & learning
│   ├── context.json          # Current session state
│   ├── memory.md            # Long-term patterns & preferences
│   ├── update_context.py    # Manual update utility
│   ├── claude_agent.py      # Autonomous feedback processor
│   ├── start_agent.sh       # Agent startup script
│   └── web/                 # Real-time viewer
│       ├── index.html       # Dashboard interface
│       └── watch.py         # File watcher server
└── README.md               # This file
```

## 🧠 How It Works

### Context Files
- **feedback.json** - Tracks user preferences, performance patterns, and real-time notes
- **context.json** - Maintains current focus, active tasks, and working memory
- **memory.md** - Stores long-term learnings and successful interaction patterns

### Real-Time Viewer
- **Web dashboard** showing current context and feedback
- **Auto-refresh** every 2 seconds to show latest changes
- **Quick feedback** input with Shift+Enter shortcut
- **File watcher** detects changes and logs them

## 🎯 Key Features

### For Claude
- **Session continuity** - Remember context between different Claude instances
- **User preference learning** - Track what works and what doesn't
- **Performance optimization** - Identify fast vs slow patterns
- **Pattern recognition** - Build on successful approaches

### For Users
- **Real-time feedback** - See progress and provide input during work sessions
- **Visual progress** - Task completion tracking and metrics
- **Low overhead** - Simple file-based system, no databases
- **Easy updates** - Multiple ways to add feedback and update context

## 🛠 Usage Examples

### Starting the Viewer
```bash
# Default port 3000
cd .claude/web && python3 watch.py

# Custom port
python3 watch.py --port 8080

# Custom path
python3 watch.py --path /path/to/.claude
```

### Manual Context Updates
```bash
# Add feedback note
python3 .claude/update_context.py feedback "Claude handled the JSON updates really well"

# Update current focus
python3 .claude/update_context.py focus "Testing the web interface" "debugging" "fix any visual issues"
```

### Web Interface Features
- **📊 Real-time metrics** - Session duration, task progress, completion rates
- **💬 Feedback log** - Recent feedback with timestamps and categories
- **🏃‍♂️ Performance notes** - Fast vs slow patterns for optimization
- **🎯 User preferences** - Tracked communication and tool preferences
- **⚡ Quick feedback** - Add notes with Shift+Enter shortcut

## 📊 Data Structure

### feedback.json Structure
```json
{
  "project_meta": {
    "name": "Claude Improvement Project",
    "last_updated": "2025-08-02T00:00:00Z",
    "session_count": 1
  },
  "current_session": {
    "session_id": "session_001", 
    "current_focus": "Current work focus",
    "active_tasks": ["Task 1", "Task 2"]
  },
  "feedback_log": [
    {
      "timestamp": "2025-08-02T00:00:00Z",
      "type": "preference|performance|insight",
      "category": "workflow|architecture|interaction",
      "note": "Descriptive feedback",
      "source": "manual|auto|pattern_analysis"
    }
  ],
  "performance_notes": {
    "fast_patterns": ["Direct file edits", "JSON updates"],
    "slow_patterns": ["Large searches", "Complex refactoring"],
    "user_preferences": {
      "communication_style": "concise and direct",
      "solution_preference": "minimal viable approach"
    }
  }
}
```

### context.json Structure
```json
{
  "current_context": {
    "active_focus": "What we're working on now",
    "progress_status": "Current state",
    "next_priority": "What to do next"
  },
  "active_decisions": [
    {
      "decision": "What was decided",
      "rationale": "Why it was decided", 
      "timestamp": "When it was decided"
    }
  ],
  "working_memory": {
    "key_files_identified": ["Important file paths"],
    "patterns_learned": ["Behavioral patterns"],
    "user_workflow": {
      "development_style": "How user likes to work",
      "preference_for_demos": "User's demo preferences"
    }
  }
}
```

## 🔧 Customization

### Port Configuration
The viewer runs on port 3000 by default. Change it if needed:
```bash
python3 watch.py --port 8080
```

### File Locations
By default, the system looks for `.claude/` in the parent directory. Override with:
```bash
python3 watch.py --path /custom/path/to/.claude
```

### Auto-refresh Rate
The web interface refreshes every 2 seconds. Modify in `index.html`:
```javascript
// Change 2000 to desired milliseconds
setInterval(loadData, 2000);
```

## 📈 Benefits

### Improved Claude Performance
- **Context awareness** across sessions
- **User preference adaptation** 
- **Performance pattern optimization**
- **Reduced repetitive explanations**

### Better User Experience  
- **Visual progress tracking**
- **Real-time feedback capability**
- **Session continuity**
- **Minimal setup overhead**

### Learning & Adaptation
- **Pattern recognition** for successful approaches
- **Preference learning** for communication style
- **Performance optimization** based on timing data
- **Long-term memory** across multiple projects

## 🏗 Implementation Notes

### Design Philosophy
- **Simple over complex** - File-based, minimal dependencies
- **Real-time updates** - Immediate feedback and context sharing
- **Pattern-based** - Build on existing successful approaches
- **Low overhead** - Maximum value with minimal setup

### Technical Choices
- **Python + HTML/JS** - Simple, reliable, easy to modify
- **JSON for data** - Human-readable, easy to edit manually
- **File watching** - Reliable change detection
- **No databases** - Reduces complexity and dependencies

### Future Enhancements
- **Automated pattern detection** using ML on feedback data
- **Integration with git** for automatic context updates
- **Browser extension** for easier feedback during Claude sessions
- **Export capabilities** for sharing learned patterns

## 🤝 Contributing

This system is designed to be:
- **Easily modifiable** - Simple code structure
- **Extensible** - Add new features by updating JSON schemas
- **Transferable** - Copy `.claude/` directory to new projects

Feel free to adapt the structure for your specific needs or extend the functionality.

## 📝 License

Built for personal productivity enhancement. Adapt and modify as needed for your Claude workflows.

---

*Built with inspiration from the HANU project's status tracking patterns. Designed for developers who want Claude to remember and adapt to their preferences over time.*