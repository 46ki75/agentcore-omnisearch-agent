# Architecture Design

## Three-Layer Agent System

This project implements a three-layer agent architecture using the Agent-to-Agent (A2A) Protocol for inter-agent communication.

```txt
┌─────────────────────────┐
│    End-User Agent       │  ← User interaction
│  (Query understanding   │
│   & Response synthesis) │
└───────────┬─────────────┘
            │ A2A
            ↓
┌─────────────────────────┐
│  Omni Search Agent      │  ← Query routing & aggregation
│  (Search orchestration) │
└───────────┬─────────────┘
            │ A2A
            ↓
┌─────────────────────────┐
│   Specialized Search    │  ← Domain-specific search
│   Agents (AWS, Azure,   │     (Verbatim quotes + URLs)
│   Microsoft, etc.)      │
└─────────────────────────┘
```

## Layer Responsibilities

### Layer 1: End-User Agent

- Receives user queries
- Delegates searches via A2A when needed
- Synthesizes natural responses from search results
- Provides source attribution

### Layer 2: Omni Search Agent

- Analyzes queries to identify required domains
- Routes searches to appropriate specialized agents
- Aggregates results from multiple agents
- Formats unified output with sources

### Layer 3: Specialized Search Agents

- Execute domain-specific searches using MCP servers
- Return verbatim quotes from official sources
- Provide complete source URLs
- No interpretation or summarization

## Communication Protocol

All inter-agent communication uses **Agent-to-Agent (A2A) Protocol**, enabling:

- Standardized message exchange
- Agent discovery and capability negotiation
- Reliable request/response patterns

## Design Benefits

- **Separation of concerns**: Each layer has a clear, focused responsibility
- **Scalability**: New specialized agents can be added without modifying other layers
- **Reliability**: Official sources via MCP servers reduce context window pressure
- **Maintainability**: Standardized A2A protocol simplifies integration
