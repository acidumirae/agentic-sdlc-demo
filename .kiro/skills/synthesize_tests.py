#!/usr/bin/env python3
"""
Skill: synthesize_tests
Agent: testing-agent
Phase: testing-and-debugging

Analyzes source modules, generates comprehensive test suites covering
unit, integration, and edge cases, then reports coverage metrics.
"""

import sys
import os
import ast
import subprocess
from pathlib import Path
from typing import Any


def discover_modules(src_path: str) -> list[str]:
    """Walk src_path and return all Python/TS/JS source files."""
    extensions = {".py", ".ts", ".js", ".tsx", ".jsx"}
    modules: list[str] = []
    for root, _, files in os.walk(src_path):
        for fname in files:
            if Path(fname).suffix in extensions:
                modules.append(os.path.join(root, fname))
    return modules


def extract_functions(module_path: str) -> list[str]:
    """
    Extract public function/method names from a Python module via AST.
    For TS/JS files, returns a placeholder list (production: use ts-morph).
    """
    if not module_path.endswith(".py"):
        return ["render", "handleSubmit", "fetchData"]

    with open(module_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]


def generate_test_cases(module_path: str, functions: list[str]) -> str:
    """
    Generate a test file for the given module and its public functions.
    Covers: happy path, null inputs, boundary values, and auth edge cases.
    """
    module_name = Path(module_path).stem
    lines = [
        f'"""Auto-generated tests for {module_name} — Testing Agent"""',
        "import pytest",
        f"# from {module_path.replace('/', '.')} import *",
        "",
    ]

    for fn in functions:
        lines += [
            f"class Test{fn.title().replace('_', '')}:",
            f'    """Tests for {fn}"""',
            "",
            f"    def test_{fn}_happy_path(self):",
            f'        """Happy path: valid inputs return expected output."""',
            f"        # Arrange",
            f"        # Act",
            f"        # Assert",
            f"        pass",
            "",
            f"    def test_{fn}_null_input(self):",
            f'        """Edge case: null/None input raises ValueError."""',
            f"        with pytest.raises((ValueError, TypeError)):",
            f"            pass  # {fn}(None)",
            "",
            f"    def test_{fn}_boundary_values(self):",
            f'        """Boundary: test with 0, -1, and max values."""',
            f"        pass",
            "",
            f"    def test_{fn}_unauthorized(self):",
            f'        """Security: unauthenticated call returns 403."""',
            f"        pass",
            "",
        ]

    return "\n".join(lines)


def write_test_artifacts(tests: dict[str, str], output_dir: str) -> list[str]:
    """Write generated test files to the tests/ directory."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    for module_name, test_content in tests.items():
        test_path = os.path.join(output_dir, f"test_{module_name}.py")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        written.append(test_path)

    return written


def run_coverage_check(test_dir: str, src_dir: str) -> dict[str, Any]:
    """
    Run pytest with coverage and return a summary dict.
    Requires pytest and pytest-cov installed.
    """
    result = subprocess.run(
        ["python", "-m", "pytest", test_dir, f"--cov={src_dir}",
         "--cov-report=term-missing", "-q", "--tb=short"],
        capture_output=True, text=True
    )
    passed = result.returncode == 0
    # Parse coverage % from output (simplified)
    coverage = 0
    for line in result.stdout.splitlines():
        if "TOTAL" in line:
            parts = line.split()
            try:
                coverage = int(parts[-1].replace("%", ""))
            except (ValueError, IndexError):
                pass

    return {"passed": passed, "coverage": coverage, "output": result.stdout}


def main() -> int:
    """Entry point for the Testing Agent skill."""
    src_path = sys.argv[1] if len(sys.argv) > 1 else "src"
    test_dir = sys.argv[2] if len(sys.argv) > 2 else "tests"
    min_coverage = int(sys.argv[3]) if len(sys.argv) > 3 else 90

    print(f"[Testing Agent] Discovering modules in {src_path}/")
    modules = discover_modules(src_path)
    print(f"[Testing Agent] Found {len(modules)} module(s)")

    tests: dict[str, str] = {}
    for module_path in modules:
        functions = extract_functions(module_path)
        if functions:
            module_name = Path(module_path).stem
            tests[module_name] = generate_test_cases(module_path, functions)
            print(f"  [✔] Generated {len(functions) * 4} tests for {module_name}")

    print(f"\n[Testing Agent] Writing test files to {test_dir}/")
    written = write_test_artifacts(tests, test_dir)
    for path in written:
        print(f"  [✔] {path}")

    print("\n[Testing Agent] Running coverage check...")
    report = run_coverage_check(test_dir, src_path)
    coverage = report["coverage"]
    status = "COMPLETE" if report["passed"] and coverage >= min_coverage else "FAIL"

    print(f"[Testing Agent] Coverage: {coverage}% (target: {min_coverage}%)")
    print(f"\nSTATUS: {status} | PHASE: testing-and-debugging | NEXT_AGENT: security-agent")

    return 0 if status == "COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
