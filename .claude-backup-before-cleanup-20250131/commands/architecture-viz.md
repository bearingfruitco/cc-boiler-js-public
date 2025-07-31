# Architecture Visualization

Generate visual representations of your system architecture using ASCII diagrams and Mermaid syntax.

## Usage

```bash
/architecture-viz [type] [--format]
/viz-arch         # alias
/av               # short alias
```

## Options

- `type`: What to visualize (system, database, api, components, flow, security)
- `--format`: Output format (ascii, mermaid, both) - default: both

## Visualization Process

I'll analyze your architecture documents and generate visual representations. Let me use the system architect to help create accurate diagrams:

```bash
# Use specialized architect for visualization
/spawn system-architect "Create visual representations of the architecture"
```

### 1. System Overview Visualization

**ASCII Diagram:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           System Architecture                            │
└─────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
     │   Browser    │         │ Mobile App   │         │   API Client │
     │   (Users)    │         │   (Users)    │         │  (External)  │
     └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
            │                        │                         │
            └────────────┬───────────┴─────────────┬──────────┘
                         │                         │
                         ▼                         ▼
                 ┌───────────────────────────────────────┐
                 │          Cloudflare CDN               │
                 │    (Static Assets & DDoS Protection)  │
                 └───────────────┬───────────────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────────────┐
                 │           Vercel Edge                 │
                 │      (Next.js Application)            │
                 │  ┌─────────────────────────────────┐ │
                 │  │   Pages    │   API    │   ISR   │ │
                 │  └─────────────────────────────────┘ │
                 └───────────────┬───────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
         ┌──────────────────┐      ┌──────────────────┐
         │  Supabase Auth   │      │ Supabase Storage │
         │  (JWT & OAuth)   │      │  (File Upload)   │
         └──────────────────┘      └──────────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────────────┐
                 │         Supabase Database             │
                 │         (PostgreSQL + RLS)            │
                 │  ┌─────────────────────────────────┐ │
                 │  │ Users │ Forms │ Results │ Audit │ │
                 │  └─────────────────────────────────┘ │
                 └───────────────┬───────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
         ┌──────────────────┐      ┌──────────────────┐
         │  Redis Cache     │      │   Event Queue    │
         │  (Session/Data)  │      │ (Async Process)  │
         └──────────────────┘      └──────────────────┘
```

**Mermaid Diagram:**
```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Browser Users]
        Mobile[Mobile App Users]
        API[API Clients]
    end
    
    subgraph "Edge Layer"
        CDN[Cloudflare CDN<br/>DDoS Protection]
        Edge[Vercel Edge<br/>Next.js SSR/SSG]
    end
    
    subgraph "Application Layer"
        Auth[Supabase Auth<br/>JWT & OAuth]
        Storage[Supabase Storage<br/>File Management]
        Functions[Edge Functions<br/>Business Logic]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL<br/>with RLS)]
        Cache[(Redis Cache<br/>Sessions)]
        Queue[Event Queue<br/>Async Jobs]
    end
    
    Browser --> CDN
    Mobile --> CDN
    API --> CDN
    CDN --> Edge
    Edge --> Auth
    Edge --> Storage
    Edge --> Functions
    Auth --> DB
    Storage --> DB
    Functions --> DB
    Functions --> Cache
    Functions --> Queue
```

### 2. Database Schema Visualization

**ASCII Diagram:**
```
┌─────────────────────┐       ┌─────────────────────┐
│      users          │       │    organizations    │
├─────────────────────┤       ├─────────────────────┤
│ id (uuid) PK        │       │ id (uuid) PK        │
│ email               │       │ name                │
│ full_name           │◄──────┤ owner_id FK         │
│ created_at          │       │ created_at          │
└─────────┬───────────┘       └─────────────────────┘
          │ 1:N                          │ 1:N
          ▼                              ▼
┌─────────────────────┐       ┌─────────────────────┐
│      forms          │       │   form_responses    │
├─────────────────────┤       ├─────────────────────┤
│ id (uuid) PK        │       │ id (uuid) PK        │
│ user_id FK          │◄──────┤ form_id FK          │
│ title               │       │ data (jsonb)        │
│ fields (jsonb)      │       │ created_at          │
└─────────────────────┘       └─────────────────────┘
```

**Mermaid ER Diagram:**
```mermaid
erDiagram
    users ||--o{ forms : creates
    users ||--o{ organizations : owns
    organizations ||--o{ forms : contains
    forms ||--o{ form_responses : receives
    
    users {
        uuid id PK
        string email UK
        string full_name
        timestamp created_at
    }
    
    organizations {
        uuid id PK
        string name
        uuid owner_id FK
        timestamp created_at
    }
    
    forms {
        uuid id PK
        uuid user_id FK
        uuid organization_id FK
        string title
        jsonb fields
        timestamp created_at
    }
    
    form_responses {
        uuid id PK
        uuid form_id FK
        jsonb data
        timestamp created_at
    }
```

### 3. API Structure Visualization

**ASCII Tree:**
```
/api
├── /auth
│   ├── POST   /login         → User authentication
│   ├── POST   /logout        → End session
│   ├── POST   /register      → Create account
│   └── GET    /me            → Current user
├── /forms
│   ├── GET    /              → List forms
│   ├── POST   /              → Create form
│   ├── GET    /:id           → Get form
│   ├── PUT    /:id           → Update form
│   ├── DELETE /:id           → Delete form
│   └── POST   /:id/submit    → Submit response
├── /analytics
│   ├── GET    /forms/:id     → Form analytics
│   └── GET    /dashboard     → Overview stats
└── /admin
    ├── GET    /users         → List users
    └── GET    /audit         → Audit logs
```

**Mermaid Sequence Diagram:**
```mermaid
sequenceDiagram
    participant C as Client
    participant E as Edge (Vercel)
    participant A as Auth (Supabase)
    participant D as Database
    participant Q as Queue
    
    C->>E: POST /api/forms
    E->>A: Verify JWT
    A-->>E: User verified
    E->>D: Insert form
    D-->>E: Form created
    E->>Q: Queue analytics
    E-->>C: 201 Created
    Q->>D: Update analytics
```

### 4. Component Hierarchy Visualization

**ASCII Tree:**
```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Container.tsx
│   ├── forms/
│   │   ├── FormBuilder.tsx
│   │   ├── FormRenderer.tsx
│   │   └── fields/
│   │       ├── TextField.tsx
│   │       ├── SelectField.tsx
│   │       └── DateField.tsx
│   ├── analytics/
│   │   ├── Dashboard.tsx
│   │   └── charts/
│   │       ├── LineChart.tsx
│   │       └── BarChart.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Modal.tsx
```

**Mermaid Graph:**
```mermaid
graph TD
    App[App]
    App --> Layout[Layout]
    App --> Pages[Pages]
    
    Layout --> Header[Header]
    Layout --> Footer[Footer]
    
    Pages --> FormBuilder[Form Builder]
    Pages --> FormViewer[Form Viewer]
    Pages --> Analytics[Analytics]
    
    FormBuilder --> FieldTypes[Field Types]
    FormViewer --> FormRenderer[Form Renderer]
    Analytics --> Charts[Charts]
    
    FieldTypes --> TextField[Text Field]
    FieldTypes --> SelectField[Select Field]
    Charts --> LineChart[Line Chart]
    Charts --> BarChart[Bar Chart]
```

### 5. Data Flow Visualization

**ASCII Flow:**
```
User Input ──► Form Builder ──► Validation ──► API
                                                │
                                                ▼
Dashboard ◄── Analytics ◄── Queue ◄── Database
```

**Mermaid Flow:**
```mermaid
flowchart LR
    U[User Input] --> FB[Form Builder]
    FB --> V{Validation}
    V -->|Valid| API[API Endpoint]
    V -->|Invalid| E[Error Message]
    API --> DB[(Database)]
    DB --> Q[Event Queue]
    Q --> A[Analytics Engine]
    A --> D[Dashboard]
    E --> U
```

### 6. Security Architecture Visualization

**ASCII Diagram:**
```
┌─────────────────────────────────────────────────────────┐
│                  Security Layers                         │
├─────────────────────────────────────────────────────────┤
│ Layer 1: Network     │ Cloudflare WAF, DDoS Protection │
├──────────────────────┼──────────────────────────────────┤
│ Layer 2: Application │ JWT Auth, CORS, Rate Limiting   │
├──────────────────────┼──────────────────────────────────┤
│ Layer 3: Database    │ RLS Policies, Encrypted Fields  │
├──────────────────────┼──────────────────────────────────┤
│ Layer 4: Monitoring  │ Audit Logs, Anomaly Detection   │
└──────────────────────┴──────────────────────────────────┘
```

**Mermaid Security Flow:**
```mermaid
graph TB
    subgraph "Threat Model"
        T1[SQL Injection]
        T2[XSS Attacks]
        T3[CSRF]
        T4[DDoS]
        T5[Data Breach]
    end
    
    subgraph "Security Controls"
        C1[Input Validation]
        C2[Output Encoding]
        C3[CSRF Tokens]
        C4[Rate Limiting]
        C5[Encryption]
    end
    
    subgraph "Monitoring"
        M1[WAF Logs]
        M2[Audit Trail]
        M3[Alerts]
    end
    
    T1 --> C1
    T2 --> C2
    T3 --> C3
    T4 --> C4
    T5 --> C5
    
    C1 --> M1
    C2 --> M2
    C3 --> M2
    C4 --> M1
    C5 --> M3
```

## Integration with Architecture Workflow

This visualization command:
- Reads from your architecture documents
- Generates both ASCII (for documentation) and Mermaid (for web rendering)
- Can be included in your architecture validation process
- Helps communicate design to stakeholders
- Updates automatically as architecture evolves

## Usage Examples

```bash
# Generate all visualizations
/architecture-viz

# Just system overview
/av system

# Database schema in Mermaid only
/av database --format=mermaid

# API structure in ASCII
/av api --format=ascii

# Quick visualization after architecture update
/chain architecture-design && /av
```

## Export Options

Generated diagrams can be:
- Copied to architecture documents
- Exported as images (Mermaid)
- Included in presentations
- Used in README files
- Added to PRDs for clarity

The visualizations help ensure everyone understands the architecture before implementation begins!
