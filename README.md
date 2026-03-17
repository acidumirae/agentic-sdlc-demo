# Agentic SDLC Framework

This repository serves as a blueprint for a fully Agentic Software Development Life Cycle (SDLC). It contains specifications, rules, AI skills, and hooks designed for agentic editors and frameworks like Cursor (`.cursor`) and Kiro (`.kiro`).

## Phases of the Agentic SDLC

1. **Requirements & Planning**: Agents act as Product Managers. They analyze vague user requests, ask clarifying questions, and output formal specifications (`spec.md`) and acceptance criteria.
2. **Architecture & Design**: Architect Agents design the system given the specifications. They define module boundaries, API contracts, and produce Mermaid diagrams.
3. **Implementation**: Developer Agents write the code exactly matching the API contracts and architectural patterns.
4. **Verification & QA**: QA Agents execute test suites, add edge-case tests, and ensure code coverage meets the requisite threshold.
5. **Review & Deployment**: Code Review Agents analyze diffs for security, performance, and style, then trigger deployment pipelines.

## Project Structure

- `.cursor/rules/`: Context-aware rules for Cursor IDE to enforce SDLC phases.
- `.cursorrules`: Global prompt rules for the agent.
- `.kiro/specifications/`: Formal definitions of the agentic workflow.
- `.kiro/skills/`: Prompt instructions giving the agent specialized capabilities (Architect, QA, etc.).
- `.kiro/hooks/`: Scripts that enforce phase barriers (e.g., stopping implementation if no spec exists).
