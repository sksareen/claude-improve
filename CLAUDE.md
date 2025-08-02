# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Project Overview

Claude Improvement Project - A workspace for developing better context management and real-time feedback systems to enhance Claude's performance and helpfulness. This project implements structured memory and feedback patterns based on successful patterns from the HANU project.

## Development Commands

```bash
# Start the real-time feedback viewer
cd .claude/web && python3 watch.py
# Then open http://localhost:3000

# Update context manually
python3 .claude/update_context.py

# No build or test commands - this uses simple file-based systems
```

## Architecture

This project uses a file-based context management system:

- **CLAUDE.md** - Main guidance file for Claude
- **.claude/** - Structured memory and feedback directory
  - **feedback.json** - Real-time feedback and notes
  - **context.json** - Current working context and state
  - **memory.md** - Long-term learnings and patterns
  - **web/** - Auto-refreshing viewer interface
- **Simple JSON updates** - Following the proven pattern from HANU status_ai.json

## Key Technical Details

1. **File-Based Memory**: Uses JSON files for structured context, MD files for documentation
2. **Real-Time Updates**: File watcher with auto-refreshing web viewer
3. **Low Overhead**: Minimal dependencies, direct file operations
4. **Pattern-Based**: Built on successful patterns from HANU project
5. **Preference Tracking**: Learns and remembers user preferences and workflow patterns

## Development Guidelines

1. **Simple File Operations**: Direct JSON/MD file updates, no databases
2. **Incremental Updates**: Small, frequent context updates rather than large batch changes
3. **Pattern Recognition**: Track what works and what doesn't for future sessions
4. **User Preferences**: Remember coding style, tool preferences, communication style
5. **Session Continuity**: Maintain context across multiple Claude sessions

## Context Management

**Auto-Updating Context Files**: This repository maintains several context files that help Claude understand current state and user preferences:

- **feedback.json** - Real-time feedback during work sessions
- **context.json** - Current focus, active tasks, decisions made
- **memory.md** - Long-term patterns, preferences, what works well

### Context Update Triggers

- Every 5-10 completed tasks
- When user provides explicit feedback
- At start/end of significant work sessions
- When discovering new user preferences
- When encountering errors or blockers

## User Preferences (Learned from HANU Project)

Based on existing patterns:
- Prefers JSON for structured data, MD for documentation
- Likes simple, minimal solutions over complex infrastructure
- Values real-time feedback and progress tracking
- Prefers functional demos over perfect architecture
- Uses keyboard shortcuts and efficiency patterns
- Values direct file edits over database operations

## Common Tasks

- **Add feedback**: Update `.claude/feedback.json` with real-time notes
- **Update context**: Modify `.claude/context.json` with current state
- **Track patterns**: Note successful approaches in `.claude/memory.md`
- **Review progress**: Use web viewer to see updates in real-time
- **Session handoff**: Update context before ending work session

## Success Criteria

- ✅ Context preserved between Claude sessions
- ✅ User preferences remembered and applied
- ✅ Real-time feedback system working
- ✅ Patterns identified and reused
- ✅ Minimal overhead for maximum value
- ✅ Seamless integration with existing workflow