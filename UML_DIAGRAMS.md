# UML Diagrams (Part 2)

This document contains the **Use Case Diagram**, **Activity Diagram**, and **Deployment Diagram** for the **AI-Based Boot Firmware and OS Boot Log Analytics** project.

## 1. Use Case Diagram

This diagram illustrates the interactions between the users (e.g., Firmware/Hardware Engineers) and the various features of the system.

```mermaid
usecaseDiagram
    actor "Firmware/Hardware Engineer" as User
    
    rectangle "AI Boot Log Analytics Platform" {
        usecase "Upload Boot Log File" as UC1
        usecase "View Analysis Dashboard" as UC2
        usecase "View Boot Timeline & Milestones" as UC3
        usecase "View ML Anomaly Score" as UC4
        usecase "Read LLM Root Cause Explanation" as UC5
        usecase "View Historical Boot Data" as UC6
    }
    
    User --> UC1
    User --> UC2
    User --> UC6
    
    UC2 ..> UC3 : <<includes>>
    UC2 ..> UC4 : <<includes>>
    UC2 ..> UC5 : <<includes>>
    
    actor "External LLM API (Gemini)" as Gemini
    UC5 <-- Gemini : Provides Explanation
```

*(Note: If the `usecaseDiagram` syntax is not fully supported by all standard markdown viewers, a flowchart representation of the Use Case is provided below for maximum compatibility.)*

```mermaid
flowchart LR
    User([Firmware/Hardware Engineer])
    
    subgraph System [AI Boot Log Analytics Platform]
        UC1(Upload Boot Log File)
        UC2(View Analysis Dashboard)
        UC3(View Boot Timeline)
        UC4(View ML Anomaly Score)
        UC5(Read LLM Root Cause)
        UC6(View Historical Reports)
    end
    
    Gemini([External LLM API / Gemini])
    
    User --> UC1
    User --> UC2
    User --> UC6
    
    UC2 -.->|includes| UC3
    UC2 -.->|includes| UC4
    UC2 -.->|includes| UC5
    
    UC5 <--> Gemini
```


## 2. Activity Diagram

This diagram shows the step-by-step workflow of the system from the moment a log file is uploaded until the dashboard is presented.

```mermaid
stateDiagram-v2
    [*] --> UploadLog
    UploadLog: User uploads Boot Log
    
    state "Log Parsing & Classification" as Parsing {
        [*] --> ParseUART
        ParseUART --> ParseKernel
        ParseKernel --> AnalyzeBootStages
    }
    
    UploadLog --> Parsing
    
    state "Machine Learning & Rules Pipeline" as Pipeline {
        [*] --> ExtractTemplates
        ExtractTemplates --> BuildFeatures
        BuildFeatures --> IsolationForest
        IsolationForest --> RuleEngine
        RuleEngine --> ConfidenceFusion
    }
    
    Parsing --> Pipeline
    
    state "Resolution & Explanation" as Resolution {
        [*] --> CheckKB
        CheckKB: High Confidence KB Match?
        CheckKB --> UseKB: Yes
        CheckKB --> QueryLLM: No
        UseKB: Use Pre-defined KB Resolution
        QueryLLM: Query Gemini LLM for Root Cause
        UseKB --> CompileReport
        QueryLLM --> CompileReport
    }
    
    Pipeline --> Resolution
    
    Resolution --> RenderDashboard
    RenderDashboard: Update React UI with JSON Data
    RenderDashboard --> [*]
```

## 3. Deployment Diagram

This diagram maps the software components to the physical/virtual hardware nodes they run on, based on the `docker-compose.yml` and project structure.

```mermaid
flowchart TD
    subgraph Client [User Device]
        Browser(Web Browser)
    end
    
    subgraph Host [Host Machine / Server]
        subgraph DockerNetwork [Internal Docker Network]
            
            subgraph FrontendNode [Frontend Container]
                React[React 18 + Vite]
            end
            
            subgraph BackendNode [Backend Container]
                FastAPI[FastAPI Server]
                SQLite[(diagnostics.db)]
                ML[Isolation Forest Models]
                Python[Python 3.10 Runtime]
            end
            
        end
    end
    
    subgraph Cloud [External Services]
        Gemini[Google Gemini API]
    end
    
    Browser -- "HTTP (Port 5173)" --> React
    React -- "REST API (Port 8000)" --> FastAPI
    
    FastAPI -- "File I/O" --> SQLite
    FastAPI -- "Loads .pkl" --> ML
    FastAPI -- "HTTPS / API Call" --> Gemini
```
