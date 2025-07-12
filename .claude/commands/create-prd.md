Create a comprehensive Product Requirements Document for: $ARGUMENTS

Structure the PRD with:

## 1. Feature Overview
- What is this feature?
- Why are we building it?
- Who will use it?

## 2. User Stories
Generate 3-5 user stories in format:
"As a [type of user], I want to [action] so that [benefit]"

## 3. Functional Requirements
List specific functionalities needed:
- Must have features
- Nice to have features
- Out of scope for v1

## 4. UI/UX Requirements
- Key screens/components needed
- User flow description
- Mobile considerations

## 5. Technical Requirements
- API endpoints needed
- Database changes
- Performance requirements
- Security considerations

## 6. Success Metrics
- How will we measure success?
- What are the KPIs?

## 7. Edge Cases & Error Handling
- What could go wrong?
- How should the system respond?

## 8. Documentation & Context Requirements
### Must Read Documentation
List with reasons why each is critical:
```
- url: [official API docs] 
  why: [specific methods/patterns we'll use]
- file: [existing code example]
  why: [pattern to follow or gotcha to avoid]
- doc: [library guide]
  section: [specific section]
  critical: [key insight that prevents errors]
```

### Research Needed
Technologies requiring documentation research:
- [ ] Technology 1 - focus areas
- [ ] Technology 2 - focus areas

Run `/research-docs "[tech1], [tech2]"` before implementation

## 9. Implementation Phases
### Phase 1: Foundation (Backend/Data)
- Database schema and models
- Core business logic
- Basic API structure

### Phase 2: Core Features
- Complete API implementation
- Frontend components
- Integration and testing

### Phase 3: Polish & Production
- Error handling
- Performance optimization
- Security hardening
- Final testing

Save as docs/project/features/$ARGUMENTS-PRD.md