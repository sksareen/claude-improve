# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Project Overview

Claude Improvement Project - A workspace for developing better context management and real-time feedback systems to enhance Claude's performance and helpfulness. This project implements structured memory and feedback patterns based on successful patterns from the HANU project.

## Development Commands

```bash
# Start the real-time feedback viewer
cd .claude/web && python3 watch.py
# Then open http://localhost:3000

# Start the autonomous Claude agent
cd .claude && ./start_agent.sh
# Or manually: python3 claude_agent.py --path .

# Update context manually (if needed)
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
- **ux_config.json** - Dynamic UX theme configuration for real-time changes
- **identity_query.json** - Agent communication for autonomous feedback processing
- **claude_agent.py** - Autonomous agent for processing user feedback and updating UX
- **Simple JSON updates** - Following the proven pattern from HANU status_ai.json

## Key Technical Details

1. **File-Based Memory**: Uses JSON files for structured context, MD files for documentation
2. **Real-Time Updates**: File watcher with auto-refreshing web viewer (2-second polling)
3. **Autonomous Agent**: Claude agent processes feedback and modifies UX automatically
4. **Dynamic UX**: Theme changes (zen, paper white, dark) applied via ux_config.json
5. **Low Overhead**: Minimal dependencies, direct file operations
6. **Pattern-Based**: Built on successful patterns from HANU project
7. **Preference Tracking**: Learns and remembers user preferences and workflow patterns
8. **Identity Query System**: Agent-to-agent communication via JSON files
9. **Operational Stats**: TTI metrics, uptime, timestamps in header for performance tracking

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

## User Preferences (Comprehensive Learning)

### UI/UX Preferences
- **Design**: Minimal border radius (1-2px), paper white calm color schemes, clean aesthetic
- **Navigation**: Tab key cycles through full-screen views (Context → Feedback → Tasks)
- **Animation**: No animations - instant, efficient interactions only
- **Input**: Enter key (not Shift+Enter) submits quick feedback
- **Settings**: Wants settings button for on-the-fly UX changes without asking me
- **Timestamps**: Likes granular last-updated timestamps on each section with relative/absolute toggle

### Technical Preferences
- **Architecture**: Simple file-based solutions over complex infrastructure, but open to Redis for performance
- **Data Format**: JSON for structured data, MD for documentation
- **Performance**: Values TTI (Time to Iterate) metrics, wants <50ms target for real-time updates
- **Feedback**: Real-time updates, progress tracking, operational stats in headers
- **Efficiency**: Keyboard shortcuts, direct file operations, minimal overhead

### Communication Style
- **Response Style**: Concise, direct responses. Dislikes explanatory preambles
- **Tool Usage**: Expects autonomous agents to work without manual intervention
- **Problem Solving**: Prefers functional demos over perfect architecture
- **Progress Tracking**: Values visual todo lists and completion tracking

## Current Session State

**Active Focus**: Autonomous agent system for real-time UX modification based on user feedback
**Progress Status**: Core infrastructure complete, debugging UX application issues
**Next Priority**: Troubleshoot frontend UX config application and verify agent autonomy

## Key Learnings This Session

### Technical Patterns That Work
- **TodoWrite tool**: Essential for complex multi-step tasks, user tracks progress visually
- **File-based context**: JSON for structured data, MD for documentation, UX config for themes
- **Real-time viewer**: Auto-refresh web interface with granular timestamps per section
- **Direct file edits**: Using Edit/MultiEdit tools for precise changes
- **Parallel tool calls**: Multiple bash commands or file reads in single response for speed
- **Agent architecture**: Continuous monitoring with identity query system works well
- **API endpoints**: Clean separation between data serving and UX config
- **Feature flags**: Boolean flags in config for enabling/disabling UI elements

### Agent Management Insights
- **Autonomous Processing**: Agent should work without manual intervention once set up
- **Identity Query System**: Works well for triggering agent actions from user feedback
- **UX Keyword Detection**: Agent can detect themes (zen/calm, paper white, dark) and features (settings, TTI, enter key)
- **Config Generation**: Agent can generate ux_config.json with proper timestamps
- **Status Tracking**: Processed queries get marked with timestamps and status updates
- **Continuous Monitoring**: 2-second polling interval for identity queries is responsive
- **File-based Communication**: JSON files work reliably for agent-to-frontend communication
- **Gap Identified**: Frontend application of UX configs may have localStorage or polling issues
- **User Expectation**: Complete autonomy - submit feedback, agent processes, changes appear automatically

## Common Tasks

- **Add feedback**: Update `.claude/feedback.json` with real-time notes or use web interface
- **Update context**: Modify `.claude/context.json` with current state
- **Track patterns**: Note successful approaches in `.claude/memory.md`
- **Review progress**: Use web viewer to see updates in real-time at http://localhost:3000
- **Agent monitoring**: Claude agent runs continuously, processes identity queries automatically
- **UX changes**: Submit feedback like 'zen colors' or 'paper white theme' and agent processes
- **Session handoff**: Update context before ending work session

## Success Criteria

- ✅ Context preserved between Claude sessions
- ✅ User preferences remembered and applied
- ✅ Real-time feedback system working with 2-second refresh
- ✅ Autonomous agent processes feedback without manual intervention
- ✅ Tab navigation working for full-screen view cycling
- ✅ Granular timestamps on all sections with fresh/stale indicators
- ✅ TTI and operational stats in header
- ✅ Identity query system for agent communication
- ✅ UX config generation for theme changes
- ✅ Enter key submits quick feedback
- ✅ Patterns identified and reused
- ✅ Minimal overhead for maximum value
- ⚠️ Frontend UX config application needs debugging
- ⚠️ Settings button for live UX changes pending
- ✅ Seamless integration with existing workflow