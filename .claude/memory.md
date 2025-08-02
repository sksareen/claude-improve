# Claude Memory - Long-term Learnings

## User Preferences & Patterns

### Communication Style
- **Concise and direct** - prefers minimal explanations, dislikes preambles/postambles
- **Action-oriented** - wants to see progress and results quickly
- **Pattern-based** - likes to build on existing successful approaches
- **No manual intervention** - expects autonomous systems to work without asking

### Technical Preferences
- **Simple over complex** - consistently chooses minimal viable solutions
- **File-based over database** - prefers JSON/MD files for data storage, but open to Redis for performance
- **Direct operations** - likes direct file edits, simple scripts, minimal dependencies
- **Real-time feedback** - values progress tracking and live updates
- **Autonomous agents** - expects agents to process feedback and make changes automatically
- **Performance metrics** - TTI (Time to Iterate) tracking, <50ms targets for real-time updates

### Workflow Patterns
- **Complete autonomy** - working demos with full end-to-end functionality
- **Iterative approach** - build, test, improve cycle
- **Pattern reuse** - extends existing successful patterns rather than starting from scratch
- **Documentation first** - comprehensive context updates before troubleshooting
- **Visual feedback** - TodoWrite for progress tracking, operational stats in headers

## Successful Interaction Patterns

### What Works Well
1. **Following established patterns** - Using structures like HANU's status_ai.json
2. **TodoWrite usage** - Essential for complex tasks, user tracks progress visually
3. **Autonomous agent architecture** - Continuous monitoring with identity query system
4. **File-based communication** - JSON files for agent-to-frontend communication
5. **Real-time web viewer** - Auto-refresh with granular timestamps and operational stats
6. **Theme detection via keywords** - Agent analyzing feedback for UX preferences
7. **Feature flags and boolean configs** - Enabling/disabling UI elements dynamically
8. **Parallel tool calls** - Multiple operations in single response for speed

### What Doesn't Work
1. **Manual intervention in autonomous systems** - User expects agents to work independently
2. **Frontend UX config application issues** - localStorage conflicts or polling problems
3. **Verbose explanations** - Long explanations without being asked
4. **Incomplete workflows** - Agent processing but changes not appearing in browser
5. **Browser refresh requirements** - Theme changes should appear without manual refresh
6. **Missing settings access** - User wants self-service UX modification capabilities

## Technical Insights

### Project Architecture Patterns
- **HANU Project**: Complex multi-component system with CLI, web interfaces, OAuth
- **Status Tracking**: Uses JSON files with timestamps, task IDs, progress tracking
- **Context Files**: CLAUDE.md files provide project-specific guidance
- **Development Style**: FastAPI + Python backends, simple frontends, minimal dependencies

### Successful Tools & Approaches
- **File watchers** for real-time updates (2-second polling works well)
- **Simple web servers** for local development with API endpoints
- **JSON structured data** with human-readable formats
- **Auto-refreshing interfaces** with granular timestamp tracking
- **Keyboard shortcuts** - Tab navigation through full-screen views
- **Identity query system** - File-based agent communication
- **UX config generation** - Automatic theme creation from keyword analysis
- **Timestamp systems** - Fresh/stale color coding with relative/absolute toggle
- **Enter key submission** - User prefers Enter over Shift+Enter for quick feedback

## Context Management Strategy

### Memory Triggers
- Update feedback.json every 5-10 completed tasks
- Update context.json when focus or priorities change
- Update memory.md when learning new user preferences
- Session handoff updates when work session ends

### Information Hierarchy
1. **Immediate context** - Current task, active focus, next steps (context.json)
2. **Session feedback** - Real-time notes, performance observations (feedback.json)
3. **Long-term patterns** - User preferences, successful approaches (memory.md)
4. **Project guidance** - Technical details, commands, architecture (CLAUDE.md)

## Future Improvement Areas

### Short-term
- ✅ Implement auto-updating web viewer (completed)
- ✅ Add keyboard shortcuts for quick feedback (Tab navigation completed)
- ❌ Fix frontend UX config application (still debugging)
- ❌ Add settings button for live UX changes (pending)
- ❌ Verify complete autonomous workflow (partially working)

### Long-term
- Agent debugging dashboard for real-time status monitoring
- Pattern recognition for code style preferences
- Automated context synthesis from multiple sessions
- Settings panel for live UX customization
- TTI performance optimization under <50ms target
- Integration with existing project status systems

## Key Learnings from Session 001

### User Expectations & Preferences
1. **Complete agent autonomy expected** - Submit feedback → agent processes → changes appear automatically
2. **Paper white calm color schemes preferred** - Minimal border radius (1-2px), clean aesthetic
3. **Performance tracking valued** - TTI metrics, uptime, operational stats in header
4. **Tab navigation essential** - Full-screen view cycling (Context → Feedback → Tasks)
5. **Settings button requested** - Self-service UX changes without bothering me
6. **Enter key for feedback submission** - Not Shift+Enter
7. **Granular timestamps important** - Last-updated on each section with fresh/stale indicators

### Technical Implementation Learnings
8. **Autonomous agent architecture works** - Continuous monitoring, identity queries, UX processing
9. **File-based communication reliable** - JSON files for agent coordination
10. **Frontend application can be tricky** - UX configs generated but not always applied
11. **Agent debugging visibility needed** - Better error handling and status reporting
12. **Complete workflow verification important** - End-to-end testing of autonomous systems

## Success Metrics

### Quantitative
- Response time to user requests
- Number of context updates per session
- Task completion rate
- User satisfaction ratings (when provided)

### Qualitative
- User continues using the system
- Requests for additional features
- Positive feedback on approach
- Integration with existing workflow

---

## Agent Management Insights

### What Works in Agent Systems
- **Continuous monitoring** with 2-second polling for identity queries
- **Keyword detection** for themes (zen/calm, paper white, dark) and features
- **Status tracking** with processed timestamps and query marking
- **Config generation** with proper JSON structure and timestamps
- **Feature flags** for enabling/disabling UI elements

### Agent System Challenges
- **Frontend application** - Generated configs not always applied in browser
- **LocalStorage conflicts** - May prevent theme reapplication
- **Polling intervals** - 3-second frontend polling may have timing issues
- **Error visibility** - Need better debugging and status reporting
- **Complete workflow verification** - Harder to test end-to-end autonomous systems

### User Agent Expectations
- **Zero manual intervention** - Agent should handle everything autonomously
- **Immediate visual feedback** - Changes should appear without page refresh
- **Self-service capabilities** - Settings button for direct UX control
- **Performance awareness** - Agent should optimize for <50ms TTI targets
- **Comprehensive processing** - Agent should understand and act on all feedback types

---

*Last updated: 2025-08-01 23:54:00 - Session 001 - Comprehensive context documentation*