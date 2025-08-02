#!/usr/bin/env python3
"""
Claude Context Updater - Manual context management utility

Quick script for updating context files when needed.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def update_feedback(note, feedback_type="manual", category="user_input"):
    """Add a feedback entry"""
    feedback_path = Path(__file__).parent / 'feedback.json'
    
    try:
        with open(feedback_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ feedback.json not found")
        return False
    
    new_entry = {
        "timestamp": datetime.now().isoformat() + 'Z',
        "type": feedback_type,
        "category": category,
        "note": note,
        "source": "manual_update"
    }
    
    data['feedback_log'].append(new_entry)
    data['project_meta']['last_updated'] = datetime.now().isoformat() + 'Z'
    
    # Keep only last 50 entries
    if len(data['feedback_log']) > 50:
        data['feedback_log'] = data['feedback_log'][-50:]
    
    with open(feedback_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Added feedback: {note}")
    return True


def update_context_focus(focus, status=None, priority=None):
    """Update current context focus and status"""
    context_path = Path(__file__).parent / 'context.json'
    
    try:
        with open(context_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ context.json not found")
        return False
    
    data['current_context']['active_focus'] = focus
    if status:
        data['current_context']['progress_status'] = status
    if priority:
        data['current_context']['next_priority'] = priority
    
    with open(context_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Updated focus: {focus}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 update_context.py feedback 'your note here'")
        print("  python3 update_context.py focus 'current focus' [status] [priority]")
        print("\nExamples:")
        print("  python3 update_context.py feedback 'Claude is working well on JSON updates'")
        print("  python3 update_context.py focus 'Testing the viewer interface' 'testing' 'debug any issues'")
        return
    
    command = sys.argv[1]
    
    if command == 'feedback' and len(sys.argv) >= 3:
        note = sys.argv[2]
        update_feedback(note)
    
    elif command == 'focus' and len(sys.argv) >= 3:
        focus = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else None
        priority = sys.argv[4] if len(sys.argv) > 4 else None
        update_context_focus(focus, status, priority)
    
    else:
        print("❌ Unknown command or missing arguments")


if __name__ == '__main__':
    main()