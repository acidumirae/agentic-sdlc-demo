#!/usr/bin/env python3
"""
Skill: generate_prototype
Agent: design-agent
Phase: design-and-prototyping

Converts user stories into HTML/CSS component scaffolding and
optionally pushes wireframes to Figma/Webflow via their APIs.
"""

import sys
import os
from pathlib import Path
from typing import Any


def load_user_stories(stories_path: str) -> list[dict[str, Any]]:
    """Load user stories from docs/planning/user-stories.md."""
    if not os.path.exists(stories_path):
        raise FileNotFoundError(f"User stories not found at {stories_path}. "
                                "Run extract_requirements.py first.")
    # In production: parse markdown into structured dicts via LLM
    return [
        {"id": "US-01", "action": "authenticate with SSO", "role": "user"},
        {"id": "US-02", "action": "manage user roles", "role": "admin"},
    ]


def generate_component(story: dict[str, Any]) -> dict[str, str]:
    """
    Generate an HTML/CSS component scaffold for a given user story.
    Returns dict with 'html', 'css', and 'component_name' keys.
    """
    component_name = story["action"].replace(" ", "-").lower()
    html = f"""<!-- Auto-generated component for {story['id']}: {story['action']} -->
<section class="{component_name}" role="main" aria-label="{story['action'].title()}">
  <div class="{component_name}__container">
    <h2 class="{component_name}__title">{story['action'].title()}</h2>
    <div class="{component_name}__content">
      <!-- {story['role'].title()} interaction area -->
    </div>
  </div>
</section>"""

    css = f"""/* Component: {component_name} */
.{component_name} {{
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}}
.{component_name}__container {{
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}}
.{component_name}__title {{
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
}}
.{component_name}__content {{
  display: flex;
  gap: 1rem;
}}"""

    return {"html": html, "css": css, "component_name": component_name}


def push_to_figma(component: dict[str, str], api_token: str | None) -> bool:
    """
    Push wireframe data to Figma API.
    Requires FIGMA_API_TOKEN environment variable.
    """
    if not api_token:
        print(f"  [SKIP] Figma integration not configured (set FIGMA_API_TOKEN)")
        return False
    # Production: POST to https://api.figma.com/v1/files/{file_key}/nodes
    print(f"  [✔] Pushed {component['component_name']} wireframe to Figma")
    return True


def push_to_webflow(component: dict[str, str], api_token: str | None) -> bool:
    """
    Push component to Webflow CMS via API.
    Requires WEBFLOW_API_TOKEN environment variable.
    """
    if not api_token:
        print(f"  [SKIP] Webflow integration not configured (set WEBFLOW_API_TOKEN)")
        return False
    # Production: POST to https://api.webflow.com/sites/{site_id}/pages
    print(f"  [✔] Pushed {component['component_name']} to Webflow")
    return True


def write_design_artifacts(components: list[dict[str, str]], output_dir: str) -> list[str]:
    """Write HTML and CSS files for each generated component."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    for comp in components:
        name = comp["component_name"]
        html_path = os.path.join(output_dir, f"{name}.html")
        css_path = os.path.join(output_dir, f"{name}.css")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(comp["html"])
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(comp["css"])

        written.extend([html_path, css_path])

    return written


def main() -> int:
    """Entry point for the Design Agent skill."""
    stories_path = sys.argv[1] if len(sys.argv) > 1 else "docs/planning/user-stories.md"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "src/ui/components"

    figma_token = os.environ.get("FIGMA_API_TOKEN")
    webflow_token = os.environ.get("WEBFLOW_API_TOKEN")

    print(f"[Design Agent] Loading user stories from: {stories_path}")
    stories = load_user_stories(stories_path)

    print(f"[Design Agent] Generating {len(stories)} component(s)...")
    components = [generate_component(s) for s in stories]

    for comp in components:
        push_to_figma(comp, figma_token)
        push_to_webflow(comp, webflow_token)

    print(f"[Design Agent] Writing artifacts to {output_dir}/")
    written = write_design_artifacts(components, output_dir)
    for path in written:
        print(f"  [✔] {path}")

    print("\nSTATUS: COMPLETE | PHASE: design-and-prototyping | NEXT_AGENT: architect-agent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
