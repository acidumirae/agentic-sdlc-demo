# Agentic SDLC Prototype Walkthrough

This document outlines the architecture and execution flow for the multi-agent Software Development Life Cycle (SDLC) prototype. 

## Overview
We have created a federated multi-agent system combining `.cursor/rules` (guiding IDE-level agent interactions) and `.kerio/` framework configurations (orchestrating Git-native hooks, workflow specs, and specialized skills).

## System Architecture

### 1. Cursor Agent Rules (`.cursor/rules/`)
We established 7 distinct agents to operate within the Cursor IDE context:

- **00-orchestration.mdc**: The primary coordinator. Directs workflow traffic, validates phase completion, and ensures sub-agents adhere to the process.
- **01-planning-agent.mdc**: Extracts user stories and BDD test requirements from raw business text.
- **02-design-agent.mdc**: Interacts with mock UI hooks to generate scaffolding for web components and prototypes.
- **03-development-agent.mdc**: The execution layer. Refactors code, builds implementations, and respects architectural guidelines.
- **04-testing-agent.mdc**: Autonomously analyzes modules, synthesizes high-coverage test suites, and patches simple bugs.
- **05-security-agent.mdc**: Performs Continuous Static Analysis (SAST), finding and fixing OWASP vulnerabilities inline.
- **06-deployment-agent.mdc**: Reads telemetry data and manages IaC for predictive, zero-downtime canary deployments.

### 2. SDLC Specifications (`.kerio/specifications/`)
- `sdlc-workflow.yaml`: Defines the chronological execution graph. Every phase (e.g., `requirements-and-planning` -> `design-and-prototyping` -> `development-and-refactoring`) is linked, ensuring dependencies are met before an agent pool is activated.
- `roles.yaml`: Enumerates agent capabilities (e.g., `sast_scanning`, `ast_refactoring`), the required underlying LLM models, and strict access controls (e.g., limiting the Testing Agent to `write_tests` and bug fixes).

### 3. Workflow Integration (`.kerio/hooks/` and `.kerio/skills/`)
The system bridges the gap between text-based AI and physical computing via executable scripts:

- **Git Hooks**:
  - `pre-commit.sh`: Invokes the Security Agent to analyze diffs prior to commit, blocking the action if vulnerabilities are detected.
  - `post-merge.sh`: Invokes the Deployment Agent when code structurally lands in `main` to evaluate risk constraints.
- **Python Skills**:
  - `extract_requirements.py`: Automates the parsing of raw spec documents into structured user stories.
  - `generate_prototype.py`: Mocks the translation of textual stories into base CSS/HTML structures.
  - `synthesize_tests.py`: Simulates reading application code and automatically generating edge-case tests.
  - `deployment_predictor.py`: Evaluates mock CI/CD telemetry to output a risk score, halting unsafe deployments automatically.

## Validation Results
- The directory tree structure for `.kerio` and `.cursor/rules` has been successfully implemented and cross-linked.
- Executable flags have been set for all `.sh` hooks and `.py` skill scripts.
- The workflow maps continuously from prompt -> requirements -> design -> code -> test -> secure -> deploy.
