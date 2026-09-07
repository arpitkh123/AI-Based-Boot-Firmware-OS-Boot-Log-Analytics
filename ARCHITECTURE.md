# System Architecture and Design Document

This document outlines the system architecture, data flow, and sequence of operations for the **AI-Based Boot Firmware and OS Boot Log Analytics** project.

## 1. System Design Architecture

The system follows a modular, decoupled architecture consisting of a React-based frontend, a FastAPI backend, and an intensive ML/Analytics core pipeline.

```mermaid
graph TD
    subgraph Client Tier
        UI[React Dashboard Frontend]
    end

    subgraph API Tier
        FastAPI[FastAPI Server]
        SQLite[(SQLite DB)]
    end

    subgraph Core Inference Pipeline
        Parsers[Log Parsers: UART, Kernel, Boot]
        Feature[Feature Engineering]
        Model[Isolation Forest ML Model]
        Rules[Deterministic Rule Engine]
        Fusion[Confidence Fusion Engine]
        LLM[LLM Explainer / Gemini]
    end

    UI -- "Uploads Log (Multipart)" --> FastAPI
    FastAPI -- "Requests Analysis" --> Parsers
    Parsers -- "Parsed Logs" --> Feature
    Parsers -- "Parsed Logs" --> Rules
    Feature -- "Feature Vector" --> Model
    Model -- "Anomaly Score" --> Fusion
    Rules -- "Rule Anomalies" --> Fusion
    Fusion -- "Fused Context" --> LLM
    LLM -- "Natural Language Root Cause" --> FastAPI
    Fusion -- "Stats & Metadata" --> FastAPI
    FastAPI -- "Stores Results" --> SQLite
    FastAPI -- "Returns JSON" --> UI
```

## 2. System Architecture (Component View)

```mermaid
classDiagram
    class Frontend {
        +React Components
        +Vite Build System
        +Upload Interface
        +Dashboard Views
    }
    class BackendAPI {
        +FastAPI
        +Routes (/api/analyze)
        +SQLite DB Connections
    }
    class InferencePipeline {
        +run(log_file)
    }
    class ParserModule {
        +UARTParser
        +KernelParser
        +BootParser
    }
    class FeatureEngineering {
        +TemplateExtractor
        +FeatureBuilder
    }
    class MLModule {
        +IsolationForestModel
        +predict_feature_vector()
    }
    class RuleEngine {
        +evaluate()
    }
    class FusionEngine {
        +calculate_confidence()
    }
    class LLMExplainer {
        +explain()
    }

    Frontend --> BackendAPI : HTTP REST
    BackendAPI --> InferencePipeline : Invokes
    InferencePipeline *-- ParserModule : Uses
    InferencePipeline *-- FeatureEngineering : Uses
    InferencePipeline *-- MLModule : Uses
    InferencePipeline *-- RuleEngine : Uses
    InferencePipeline *-- FusionEngine : Uses
    InferencePipeline *-- LLMExplainer : Uses
```

## 3. Data Flow Diagram (DFD)

The following diagram illustrates how raw text log data is transformed into numerical features, scored for anomalies, and finally converted into plain-english insights.

```mermaid
flowchart TD
    RawLog((Raw Boot Log\nUART/dmesg)) --> |File Upload| LogUpload[Backend API]
    LogUpload --> Parsers(Log Parsers)
    
    Parsers --> |UART Logs| UartClassifier(UART Classifier)
    Parsers --> |Kernel Logs| KernelClassifier(Kernel Classifier)
    
    UartClassifier --> BootAnalysis(Boot Stage Analysis)
    KernelClassifier --> BootAnalysis
    
    BootAnalysis --> TemplateExtractor(Template Extraction)
    BootAnalysis --> RuleEngine(Rule Engine)
    
    TemplateExtractor --> FeatureBuilder(Feature Vector Builder)
    FeatureBuilder --> |Numerical Vector| IForest(Isolation Forest)
    
    IForest --> |ML Anomaly Score| FusionEngine(Confidence Fusion)
    RuleEngine --> |Deterministic Rule Hits| FusionEngine
    
    FusionEngine --> |Fused Confidence Score| CheckLLM{High Confidence\nKB Match?}
    
    CheckLLM -- Yes --> KBypass[Use KB Resolution]
    CheckLLM -- No --> LLM(LLM Explainer)
    
    KBypass --> JSONRes(JSON Response Builder)
    LLM --> |Root Cause Explanation| JSONRes
    
    JSONRes --> Dashboard((React Dashboard / User))
```

## 4. Sequence Diagram

This sequence diagram depicts the chronological execution flow when a user uploads a log file for analysis.

```mermaid
sequenceDiagram
    participant User
    participant Frontend as React Dashboard
    participant Backend as FastAPI
    participant Parsers as Parsers (UART/Kernel/Boot)
    participant FeatureEng as Feature Engineering
    participant ML_Model as Isolation Forest
    participant Rules as Rule Engine
    participant Fusion as Confidence Fusion
    participant LLM as LLM / Gemini

    User->>Frontend: Upload Boot Log File
    Frontend->>Backend: POST /api/analyze
    Backend->>Parsers: parse_file(log_file)
    Parsers-->>Backend: Parsed & Classified Logs
    Backend->>Parsers: analyze_boot(classified_logs)
    Parsers-->>Backend: Boot Analysis Context
    Backend->>FeatureEng: extract_templates() & build_features()
    FeatureEng-->>Backend: Generated Feature Vector
    Backend->>ML_Model: predict_feature_vector(feature_vector)
    ML_Model-->>Backend: ML Anomaly Score
    Backend->>Rules: evaluate(classified_logs, boot_analysis)
    Rules-->>Backend: Rule Matches / Known Errors
    Backend->>Fusion: calculate_confidence()
    Fusion-->>Backend: Combined Anomaly Strength
    
    alt Known Knowledge Base Failure
        Backend->>Backend: Bypass LLM, construct KB resolution
    else Unseen / Complex Anomaly
        Backend->>LLM: explain(boot_analysis, anomaly_result)
        LLM-->>Backend: Natural Language Root Cause
    end
    
    Backend->>Frontend: JSON Analysis Report
    Frontend->>User: Render Visual Dashboard
```
