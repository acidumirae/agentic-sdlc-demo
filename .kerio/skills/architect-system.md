---
name: architect-system
description: Grants the agent the ability to design software architecture.
version: 1.0.0
---

# Skill: architect-system

## Purpose
Use this skill when transitioning from the Planning Phase to the Implementation phase. This skill allows you to transform business requirements into technical blueprints.

## Instructions
1. **Read Specifications**: Find the relevant `.md` files in `docs/specs/`.
2. **Identify Entities & Relations**: Map out the data model.
3. **Draft API**: Define REST/GraphQL/RPC endpoints.
4. **Diagram**: Write Mermaid code to visualize system architecture and sequence flows.
5. **Output**: Write your findings into `docs/arch/latest_architecture.md`.

## Constraints
- Do not write implementation code (no `src/` files) while using this skill.
- Keep dependencies to a minimum unless explicitly requested.
