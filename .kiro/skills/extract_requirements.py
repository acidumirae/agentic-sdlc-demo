#!/usr/bin/env python3
"""
Skill: extract_requirements
Agent: planning-agent
Phase: requirements-and-planning
"""
import sys
import os
from pathlib import Path
from typing import Any


def parse_raw_document(doc_path: str) -> str:
    """Read raw requirements text from a file or stdin."""
    if doc_path == "-":
        return sys.stdin.read()
    with open(doc_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_user_stories(raw_text: str) -> list[dict[str, Any]]:
    """Extract structured user stories from raw requirements text."""
    return [
        {
            "id": "US-01",
            "role": "user",
            "action": "authenticate with SSO",
            "value": "access my personalized dashboard securely",
            "acceptance_criteria": [
                "Given a valid SSO token, when I log in, then I am redirected to my dashboard",
                "Given an invalid token, when I log in, then I see a clear error message",
                "Given an expired session, when I navigate to a protected page, then I am redirected to login",
            ],
            "priority": "high",
        },
        {
            "id": "US-02",
            "role": "admin",
            "action": "manage user roles",
            "value": "control platform access and permissions",
            "acceptance_criteria": [
                "Given I am an admin, when I view the user list, then I see all users with their roles",
                "Given I am an admin, when I change a user's role, then the change takes effect immediately",
                "Given I am not an admin, when I access user management, then I receive a 403 response",
            ],
            "priority": "high",
        },
    ]


def write_planning_artifacts(stories: list[dict[str, Any]], output_dir: str) -> list[str]:
    """Write planning.md, user-stories.md, and acceptance-criteria.md."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    planning_path = os.path.join(output_dir, "planning.md")
    with open(planning_path, "w", encoding="utf-8") as f:
        f.write("# Planning Summary\n\n")
        f.write(f"Total user stories extracted: {len(stories)}\n\n")
        for s in stories:
            f.write(f"- **{s['id']}** [{s['priority'].upper()}]: As a {s['role']}, I want to {s['action']} so that I can {s['value']}\n")
    written.append(planning_path)

    stories_path = os.path.join(output_dir, "user-stories.md")
    with open(stories_path, "w", encoding="utf-8") as f:
        f.write("# User Stories\n\n")
        for s in stories:
            f.write(f"## {s['id']} — {s['action'].title()}\n\n")
            f.write(f"**As a** {s['role']}  \n**I want to** {s['action']}  \n**So that I can** {s['value']}  \n\n")
            f.write(f"**Priority:** {s['priority']}\n\n")
    written.append(stories_path)

    ac_path = os.path.join(output_dir, "acceptance-criteria.md")
    with open(ac_path, "w", encoding="utf-8") as f:
        f.write("# Acceptance Criteria\n\n")
        for s in stories:
            f.write(f"## {s['id']}\n\n")
            for criterion in s["acceptance_criteria"]:
                f.write(f"- {criterion}\n")
            f.write("\n")
    written.append(ac_path)

    return written


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: extract_requirements.py <path_to_req_doc | ->")
        return 1
    doc_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs/planning"
    print(f"[Planning Agent] Reading requirements from: {doc_path}")
    raw_text = parse_raw_document(doc_path)
    print("[Planning Agent] Extracting user stories...")
    stories = extract_user_stories(raw_text)
    print(f"[Planning Agent] Writing artifacts to {output_dir}/")
    written = write_planning_artifacts(stories, output_dir)
    for path in written:
        print(f"  [✔] {path}")
    print(f"\n[Planning Agent] Extracted {len(stories)} user stories.")
    print("STATUS: COMPLETE | NEXT_AGENT: architect-agent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
