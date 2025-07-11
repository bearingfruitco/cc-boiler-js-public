Generate a detailed task list from PRD: $ARGUMENTS

Read docs/project/features/$ARGUMENTS-PRD.md and create:

## Task List for $ARGUMENTS

### Phase 1: Foundation (Backend/Data)
1.1 [ ] Create database schema
1.2 [ ] Set up API routes structure
1.3 [ ] Implement data models
1.4 [ ] Add validation schemas

### Phase 2: Core Functionality
2.1 [ ] Implement main business logic
2.2 [ ] Create service layer
2.3 [ ] Add error handling
2.4 [ ] Write unit tests

### Phase 3: User Interface
3.1 [ ] Create UI components
3.2 [ ] Implement forms
3.3 [ ] Add loading states
3.4 [ ] Handle errors in UI

### Phase 4: Integration
4.1 [ ] Connect frontend to API
4.2 [ ] Add real-time updates
4.3 [ ] Implement caching
4.4 [ ] Test full flow

### Phase 5: Polish
5.1 [ ] Add animations
5.2 [ ] Optimize performance
5.3 [ ] Improve accessibility
5.4 [ ] Final testing

Rules:
- Each task should be completable in 5-15 minutes
- Each task should produce verifiable output
- Tasks should be independent when possible
- Include task dependencies where needed

Save as docs/project/features/$ARGUMENTS-tasks.md