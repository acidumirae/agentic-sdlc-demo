#!/usr/bin/env python3

def generate_prototype(story_id):
    """
    Simulates generating a UI component structure from a Planning Agent's User Story.
    Called by the Design Agent.
    """
    print(f"[Design Agent] Generating prototype for User Story {story_id}...")
    
    # Mock CSS/HTML generation
    html_mock = f"<!-- Auto-generated layout for {story_id} -->\n<div class='container'>\n</div>"
    css_mock = ".container { display: flex; }"
    
    print("[✔] Generated wireframe and CSS. Accessible in src/ui/components/")
    return html_mock, css_mock

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: generate_prototype.py <story_id>")
        sys.exit(1)
        
    generate_prototype(sys.argv[1])
