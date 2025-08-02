# Claude Memory - Long-term Learnings

## User Preferences & Patterns

### Communication Style
- **Concise and direct** - prefers minimal explanations unless asked for details
- **Action-oriented** - wants to see progress and results quickly
- **Pattern-based** - likes to build on existing successful approaches

### Technical Preferences
- **Simple over complex** - consistently chooses minimal viable solutions
- **File-based over database** - prefers JSON/MD files for data storage
- **Direct operations** - likes direct file edits, simple scripts, minimal dependencies
- **Real-time feedback** - values progress tracking and live updates

### Workflow Patterns
- **Functionality-first** - working demos over perfect architecture
- **Iterative approach** - build, test, improve cycle
- **Pattern reuse** - extends existing successful patterns rather than starting from scratch
- **Documentation** - maintains good documentation but keeps it practical

## Successful Interaction Patterns

### What Works Well
1. **Following established patterns** - Using structures like HANU's status_ai.json
2. **TodoWrite usage** - User appreciates task tracking and progress visibility
3. **Incremental progress** - Small, frequent updates rather than large changes
4. **Context awareness** - Understanding existing project structure before making changes
5. **Low-effort solutions** - Simple implementations that provide high value

### What Doesn't Work
1. **Over-engineering** - Complex solutions when simple ones suffice
2. **Database assumptions** - Suggesting databases when files work fine
3. **Verbose explanations** - Long explanations without being asked
4. **Ignoring existing patterns** - Not leveraging established project structures

## Technical Insights

### Project Architecture Patterns
- **HANU Project**: Complex multi-component system with CLI, web interfaces, OAuth
- **Status Tracking**: Uses JSON files with timestamps, task IDs, progress tracking
- **Context Files**: CLAUDE.md files provide project-specific guidance
- **Development Style**: FastAPI + Python backends, simple frontends, minimal dependencies

### Successful Tools & Approaches
- **File watchers** for real-time updates
- **Simple web servers** for local development
- **JSON structured data** with human-readable formats
- **Auto-refreshing interfaces** for development feedback
- **Keyboard shortcuts** and efficiency patterns

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
- Implement auto-updating web viewer
- Add keyboard shortcuts for quick feedback
- Create session handoff automation

### Long-term
- Pattern recognition for code style preferences
- Automated context synthesis from multiple sessions
- Integration with existing project status systems

## Key Learnings from Session 001

1. **User has sophisticated existing systems** - HANU project shows advanced understanding of development patterns
2. **Preference for building on existing work** - Rather than creating new systems, extend successful ones
3. **Real-time feedback is highly valued** - User specifically requested this capability
4. **Simple file-based solutions preferred** - Chose JSON/MD over Redis/database options
5. **Pattern consistency matters** - Following established conventions increases adoption

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

*Last updated: 2025-08-02 - Session 001*