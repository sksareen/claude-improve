#!/usr/bin/env python3
"""
Claude Agent - Monitors identity queries and processes user feedback autonomously

This script runs continuously, watching for identity_query.json files and 
processing them to update context, preferences, and take actions based on user feedback.
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path


class ClaudeAgent:
    def __init__(self, claude_dir):
        self.claude_dir = Path(claude_dir)
        self.identity_query_path = self.claude_dir / 'identity_query.json'
        self.feedback_path = self.claude_dir / 'feedback.json'
        self.context_path = self.claude_dir / 'context.json'
        self.memory_path = self.claude_dir / 'memory.md'
        self.ux_config_path = self.claude_dir / 'ux_config.json'
        self.processed_queries = set()
        
    def watch_for_queries(self):
        """Main loop - watch for identity queries and process them"""
        print("🤖 Claude Agent started - watching for feedback to process...")
        print(f"📁 Monitoring: {self.claude_dir}")
        print("🔄 Press Ctrl+C to stop\n")
        
        while True:
            try:
                if self.identity_query_path.exists():
                    with open(self.identity_query_path, 'r') as f:
                        query = json.load(f)
                    
                    query_id = f"{query['timestamp']}_{query.get('feedback_content', '')[:20]}"
                    
                    if query_id not in self.processed_queries and query.get('status') == 'pending':
                        print(f"⚡ Processing feedback: '{query['feedback_content'][:50]}...'")
                        self.process_identity_query(query)
                        self.mark_query_processed(query)
                        self.processed_queries.add(query_id)
                        
                time.sleep(2)  # Check every 2 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Claude Agent stopped")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)
    
    def process_identity_query(self, query):
        """Process the identity query and update relevant files"""
        feedback_content = query.get('feedback_content', '')
        timestamp = query.get('timestamp', datetime.now().isoformat() + 'Z')
        
        # Analyze feedback content and determine actions
        actions = self.analyze_feedback(feedback_content)
        
        for action in actions:
            if action['type'] == 'update_preferences':
                self.update_preferences(action['data'])
            elif action['type'] == 'update_context':
                self.update_context(action['data'])
            elif action['type'] == 'add_insight':
                self.add_insight(action['data'])
            elif action['type'] == 'update_performance':
                self.update_performance_notes(action['data'])
            elif action['type'] == 'update_ux':
                self.update_ux_config(action['data'])
        
        print(f"✅ Processed {len(actions)} actions from feedback")
    
    def analyze_feedback(self, feedback):
        """Analyze feedback content and determine what actions to take"""
        feedback_lower = feedback.lower()
        actions = []
        
        # UX Theme changes (priority over general UI preferences)
        ux_updates = {}
        
        # Theme detection
        if any(word in feedback_lower for word in ['zen', 'calm', 'peaceful', 'soothing']):
            ux_updates.update({
                'theme': 'zen_mode',
                'background_color': '#0a0f0a',
                'panel_color': '#1a251a',
                'text_color': '#d0e0d0',
                'accent_color': '#6b9a6b',
                'border_color': '#2a4a2a'
            })
        elif any(word in feedback_lower for word in ['paper', 'white', 'light', 'bright']):
            ux_updates.update({
                'theme': 'paper_white',
                'background_color': '#fefefe',
                'panel_color': '#f8f8f8',
                'text_color': '#2a2a2a',
                'accent_color': '#4a9eff',
                'border_color': '#e0e0e0'
            })
        elif any(word in feedback_lower for word in ['dark', 'darker', 'black']):
            ux_updates.update({
                'theme': 'dark_mode',
                'background_color': '#000000',
                'panel_color': '#111111',
                'text_color': '#ffffff'
            })
        
        # Feature flags
        if any(word in feedback_lower for word in ['settings', 'customize', 'config']):
            ux_updates['show_settings'] = True
        
        if any(word in feedback_lower for word in ['tti', 'uptime', 'header']):
            ux_updates['fix_header_metrics'] = True
            
        if any(word in feedback_lower for word in ['enter', 'key', 'feedback', 'entry']):
            ux_updates['fix_enter_key'] = True
        
        # If UX changes detected, add UX update action
        if ux_updates:
            actions.append({
                'type': 'update_ux',
                'data': ux_updates
            })
            print(f"   🎨 Detected UX changes: {list(ux_updates.keys())}")
        
        # UI/Design preferences (for general feedback)
        elif any(word in feedback_lower for word in ['ui', 'design', 'look', 'appearance', 'visual']):
            actions.append({
                'type': 'update_preferences',
                'data': {
                    'category': 'ui_design',
                    'preference': feedback
                }
            })
        
        # Performance feedback
        if any(word in feedback_lower for word in ['slow', 'fast', 'performance', 'speed', 'lag']):
            pattern_type = 'slow_patterns' if any(word in feedback_lower for word in ['slow', 'lag', 'stuck']) else 'fast_patterns'
            actions.append({
                'type': 'update_performance',
                'data': {
                    'pattern_type': pattern_type,
                    'pattern': feedback
                }
            })
        
        # Feature requests or issues
        if any(word in feedback_lower for word in ['bug', 'issue', 'problem', 'broken', 'not working']):
            actions.append({
                'type': 'add_insight',
                'data': {
                    'category': 'areas_for_improvement',
                    'insight': feedback
                }
            })
        
        # Positive feedback about what works
        if any(word in feedback_lower for word in ['good', 'great', 'works', 'like', 'love', 'perfect']):
            actions.append({
                'type': 'add_insight',
                'data': {
                    'category': 'successful_patterns',
                    'insight': feedback
                }
            })
        
        # Context updates
        if any(word in feedback_lower for word in ['focus', 'working on', 'next', 'priority']):
            actions.append({
                'type': 'update_context',
                'data': {
                    'type': 'focus_update',
                    'content': feedback
                }
            })
        
        # Default action if no specific category
        if not actions:
            actions.append({
                'type': 'add_insight',
                'data': {
                    'category': 'general_feedback',
                    'insight': feedback
                }
            })
        
        return actions
    
    def update_preferences(self, data):
        """Update user preferences in feedback.json"""
        try:
            with open(self.feedback_path, 'r') as f:
                feedback_data = json.load(f)
            
            if 'performance_notes' not in feedback_data:
                feedback_data['performance_notes'] = {'user_preferences': {}}
            
            if 'user_preferences' not in feedback_data['performance_notes']:
                feedback_data['performance_notes']['user_preferences'] = {}
            
            # Update preference
            category = data['category']
            preference = data['preference']
            feedback_data['performance_notes']['user_preferences'][category] = preference
            
            # Update timestamp
            feedback_data['project_meta']['last_updated'] = datetime.now().isoformat() + 'Z'
            
            with open(self.feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            print(f"   📝 Updated {category} preference")
            
        except Exception as e:
            print(f"   ❌ Error updating preferences: {e}")
    
    def update_context(self, data):
        """Update context.json with new information"""
        try:
            with open(self.context_path, 'r') as f:
                context_data = json.load(f)
            
            if data['type'] == 'focus_update':
                # Add to recent completions or update focus
                completion = {
                    "task": f"User feedback: {data['content']}",
                    "completed_at": datetime.now().isoformat() + 'Z',
                    "notes": "User-provided feedback processed by agent"
                }
                
                if 'recent_completions' not in context_data:
                    context_data['recent_completions'] = []
                
                context_data['recent_completions'].insert(0, completion)
                
                # Keep only last 5 completions
                context_data['recent_completions'] = context_data['recent_completions'][:5]
            
            with open(self.context_path, 'w') as f:
                json.dump(context_data, f, indent=2)
            
            print(f"   📝 Updated context with {data['type']}")
            
        except Exception as e:
            print(f"   ❌ Error updating context: {e}")
    
    def add_insight(self, data):
        """Add insights to feedback.json"""
        try:
            with open(self.feedback_path, 'r') as f:
                feedback_data = json.load(f)
            
            if 'insights' not in feedback_data:
                feedback_data['insights'] = {
                    'successful_patterns': [],
                    'areas_for_improvement': []
                }
            
            category = data['category']
            insight = data['insight']
            
            if category not in feedback_data['insights']:
                feedback_data['insights'][category] = []
            
            # Add insight if not already present
            if insight not in feedback_data['insights'][category]:
                feedback_data['insights'][category].append(insight)
                
                # Keep only last 10 insights per category
                feedback_data['insights'][category] = feedback_data['insights'][category][-10:]
            
            # Update timestamp
            feedback_data['project_meta']['last_updated'] = datetime.now().isoformat() + 'Z'
            
            with open(self.feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            print(f"   💡 Added insight to {category}")
            
        except Exception as e:
            print(f"   ❌ Error adding insight: {e}")
    
    def update_performance_notes(self, data):
        """Update performance patterns in feedback.json"""
        try:
            with open(self.feedback_path, 'r') as f:
                feedback_data = json.load(f)
            
            if 'performance_notes' not in feedback_data:
                feedback_data['performance_notes'] = {
                    'fast_patterns': [],
                    'slow_patterns': []
                }
            
            pattern_type = data['pattern_type']
            pattern = data['pattern']
            
            if pattern_type not in feedback_data['performance_notes']:
                feedback_data['performance_notes'][pattern_type] = []
            
            # Add pattern if not already present
            if pattern not in feedback_data['performance_notes'][pattern_type]:
                feedback_data['performance_notes'][pattern_type].append(pattern)
                
                # Keep only last 10 patterns
                feedback_data['performance_notes'][pattern_type] = feedback_data['performance_notes'][pattern_type][-10:]
            
            # Update timestamp
            feedback_data['project_meta']['last_updated'] = datetime.now().isoformat() + 'Z'
            
            with open(self.feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            print(f"   ⚡ Updated {pattern_type}")
            
        except Exception as e:
            print(f"   ❌ Error updating performance notes: {e}")
    
    def mark_query_processed(self, query):
        """Mark the identity query as processed"""
        try:
            query['status'] = 'processed'
            query['processed_at'] = datetime.now().isoformat() + 'Z'
            
            with open(self.identity_query_path, 'w') as f:
                json.dump(query, f, indent=2)
            
        except Exception as e:
            print(f"   ❌ Error marking query as processed: {e}")
    
    def update_ux_config(self, data):
        """Update UX configuration file for real-time theme changes"""
        try:
            # Load existing UX config
            if self.ux_config_path.exists():
                with open(self.ux_config_path, 'r') as f:
                    config = json.load(f)
            else:
                config = {
                    'theme': 'default',
                    'colors': {},
                    'features': {},
                    'last_updated': None
                }
            
            # Apply updates
            for key, value in data.items():
                if key == 'theme':
                    config['theme'] = value
                elif key.endswith('_color'):
                    config['colors'][key] = value
                elif key.startswith('show_') or key.startswith('fix_'):
                    if 'features' not in config:
                        config['features'] = {}
                    config['features'][key] = value
                else:
                    config[key] = value
            
            config['last_updated'] = datetime.now().isoformat() + 'Z'
            
            # Save config
            with open(self.ux_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"   🎨 Updated UX config: {data.get('theme', 'features')}")
            
        except Exception as e:
            print(f"   ❌ Error updating UX config: {e}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Agent - Process user feedback autonomously')
    parser.add_argument('--path', type=str, default='.', help='Path to .claude directory')
    
    args = parser.parse_args()
    
    claude_dir = Path(args.path).resolve()
    if not claude_dir.exists():
        print(f"❌ Directory {claude_dir} does not exist")
        return
    
    agent = ClaudeAgent(claude_dir)
    agent.watch_for_queries()


if __name__ == '__main__':
    main()