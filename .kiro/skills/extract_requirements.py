#!/usr/bin/env python3

import sys
import json

def extract_requirements(doc_path):
    """
    Simulates extracting structured User Stories from a raw requirements document.
    Called by the Planning Agent.
    """
    print(f"[Planning Agent] Extracting requirements from {doc_path}...")
    
    # Mock extracted user stories
    stories = [
        {"id": "US-01", "role": "user", "action": "login", "value": "access my dashboard"},
        {"id": "US-02", "role": "admin", "action": "manage users", "value": "moderate the platform"}
    ]
    
    output_file = "docs/planning/planning.md"
    print(f"[✔] Extracted {len(stories)} stories. Writing to {output_file}.")
    
    # In a real scenario, this would generate markdown and save it.
    return stories

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_requirements.py <path_to_req_doc>")
        sys.exit(1)
    
    extract_requirements(sys.argv[1])
