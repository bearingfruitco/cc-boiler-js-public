---
name: visualize-flow
description: Visualize agent orchestration flow with Mermaid diagrams
argument-hint: [session-id | --current | --last]
allowed-tools: Read, Write, CreateFile, Bash
aliases: ["vf", "flow-viz", "agent-flow"]
---

# 🔍 Agent Orchestration Flow Visualizer

Visualizing flow for: **$ARGUMENTS**

## Generating Flow Diagram

!`python3 << 'PYTHON'
import json
import sys
from pathlib import Path
from datetime import datetime

# Parse arguments
args = """$ARGUMENTS""".strip()
if not args or args == "--current":
    session_type = "current"
elif args == "--last":
    session_type = "last"
else:
    session_type = "specific"
    session_id = args

# Paths
orchestration_dir = Path(".claude/orchestration")
temp_dir = Path(".claude/temp")
orchestration_dir.mkdir(exist_ok=True)

def load_session_data():
    """Load orchestration session data"""
    if session_type == "current":
        session_file = temp_dir / "orchestration_result.json"
        if not session_file.exists():
            print("ℹ️ No current orchestration session found.")
            print("Run `/orch [task]` to start an orchestration.")
            return None
    elif session_type == "last":
        # Find most recent session
        sessions = list(temp_dir.glob("session_orch_*.json"))
        if not sessions:
            print("ℹ️ No orchestration sessions found.")
            return None
        session_file = max(sessions, key=lambda p: p.stat().st_mtime)
    else:
        # Specific session
        session_file = temp_dir / f"session_{session_id}.json"
        if not session_file.exists():
            print(f"❌ Session '{session_id}' not found.")
            return None
    
    try:
        with open(session_file, 'r') as f:
            return json.load(f)
    except:
        return None

def generate_mermaid_diagram(session_data):
    """Generate Mermaid diagram from session data"""
    if not session_data:
        return None
    
    diagram = ["graph TD"]
    diagram.append("    Start[User Request] --> Orchestrator{Orchestrator}")
    
    # Add agents and their connections
    agents = session_data.get('agents', [])
    if not agents:
        # Use mock data for demonstration
        agents = [
            ("pm-orchestrator", "Requirements Analysis"),
            ("backend", "API Implementation"),
            ("frontend", "UI Development"),
            ("qa", "Testing & Validation")
        ]
    
    # Create agent nodes
    for i, (agent, task) in enumerate(agents):
        agent_id = f"Agent{i}"
        diagram.append(f'    Orchestrator --> {agent_id}["{agent}<br/>{task}"]')
        
        # Add sub-tasks if available
        if i > 0:
            prev_id = f"Agent{i-1}"
            diagram.append(f"    {prev_id} -.->|context| {agent_id}")
    
    # Add completion node
    diagram.append(f"    Agent{len(agents)-1} --> Complete[✓ Task Complete]")
    
    # Add styling
    diagram.extend([
        "",
        "    classDef orchestrator fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
        "    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px",
        "    classDef complete fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px",
        "",
        "    class Orchestrator orchestrator",
        "    class Agent0,Agent1,Agent2,Agent3 agent",
        "    class Complete complete"
    ])
    
    return "\n".join(diagram)

def generate_sequence_diagram(session_data):
    """Generate sequence diagram for agent communication"""
    diagram = ["sequenceDiagram"]
    diagram.append("    participant U as User")
    diagram.append("    participant O as Orchestrator")
    
    agents = ["PM", "Backend", "Frontend", "QA"]
    for agent in agents:
        diagram.append(f"    participant {agent[0]} as {agent}")
    
    # Add interactions
    diagram.append("")
    diagram.append("    U->>O: Request Feature")
    diagram.append("    O->>P: Analyze Requirements")
    diagram.append("    P-->>O: Requirements Doc")
    diagram.append("    O->>B: Implement API")
    diagram.append("    B-->>O: API Complete")
    diagram.append("    O->>F: Build UI")
    diagram.append("    F-->>O: UI Complete")
    diagram.append("    O->>Q: Run Tests")
    diagram.append("    Q-->>O: Tests Pass")
    diagram.append("    O-->>U: Feature Complete")
    
    return "\n".join(diagram)

# Load session data
session_data = load_session_data()

if session_data:
    print(f"## 📊 Orchestration Session: {session_data.get('session_id', 'Unknown')}")
    print(f"**Task**: {session_data.get('task', 'Unknown')}")
    print(f"**Started**: {session_data.get('started_at', 'Unknown')}")
    print("")

# Generate diagrams
flow_diagram = generate_mermaid_diagram(session_data)
sequence_diagram = generate_sequence_diagram(session_data)

if flow_diagram:
    print("## 🔄 Agent Flow Diagram\n")
    print("```mermaid")
    print(flow_diagram)
    print("```")
    
    # Save to file
    diagram_file = orchestration_dir / f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(diagram_file, 'w') as f:
        f.write(f"# Orchestration Flow\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("```mermaid\n")
        f.write(flow_diagram)
        f.write("\n```")
    
    print(f"\n💾 Saved to: {diagram_file}")

print("\n## 🔀 Agent Communication Sequence\n")
print("```mermaid")
print(sequence_diagram)
print("```")

# Generate context flow
print("\n## 📦 Context Flow Analysis\n")

if session_data and 'outputs' in session_data:
    outputs = session_data['outputs']
    print("| From Agent | To Agent | Context Passed |")
    print("|------------|----------|----------------|")
    
    # Mock data for demonstration
    context_flows = [
        ("pm-orchestrator", "backend", "API requirements, endpoints"),
        ("backend", "frontend", "API contracts, data models"),
        ("frontend", "qa", "UI components, test scenarios"),
        ("pm-orchestrator", "all", "Success criteria, constraints")
    ]
    
    for from_agent, to_agent, context in context_flows:
        print(f"| {from_agent} | {to_agent} | {context} |")
else:
    print("ℹ️ No context flow data available. Run an orchestration to see real data.")

print("\n## 💡 Visualization Tips\n")
print("- Copy Mermaid diagrams to view in any Mermaid renderer")
print("- Use `/trace [task]` for real-time execution tracing")
print("- Run `/debug-orchestration` for detailed debugging mode")
print("- Check `.claude/orchestration/` for saved diagrams")

PYTHON`

## Next Steps

- Real-time trace: `/trace "build user dashboard"`
- Debug mode: `/debug-orchestration on`
- View saved diagrams: `ls .claude/orchestration/`
- Generate dependency graph: `/agent-deps`
