import pytest
import yaml
import os
from pathlib import Path
from toolbox.core.workflow import WorkflowRunner
from toolbox.cli import cli

def test_variable_substitution():
    runner = WorkflowRunner(cli)
    runner.variables = {"input": "test.jpg", "ext": "png"}
    
    # Test {var} style
    result = runner._substitute_vars("image convert {input} {input.stem}.{ext}")
    assert result == "image convert test.jpg test.png"
    
    # Test $VAR style
    result = runner._substitute_vars("image convert $input ${input.stem}.$ext")
    assert result == "image convert test.jpg test.png"

def test_dry_run_workflow():
    # Use a local filename for testing to avoid PermissionError in temp dirs
    wf_path = Path("test_wf.yaml")
    wf_data = {
        "name": "Test Workflow",
        "vars": {"file": "input.jpg"},
        "steps": [
            {"name": "Step 1", "command": "image metadata {file}"}
        ]
    }
    try:
        with open(wf_path, "w") as f:
            yaml.dump(wf_data, f)
            
        runner = WorkflowRunner(cli)
        # This should not fail if dry_run works
        runner.run(str(wf_path), dry_run=True)
    finally:
        if wf_path.exists():
            wf_path.unlink()

def test_condition_skipping():
    wf_path = Path("skip_wf.yaml")
    wf_data = {
        "name": "Skip Workflow",
        "vars": {"do_it": "false"},
        "steps": [
            {"name": "Should Skip", "command": "image info input.jpg", "if": "{do_it}"}
        ]
    }
    try:
        with open(wf_path, "w") as f:
            yaml.dump(wf_data, f)
            
        runner = WorkflowRunner(cli)
        # Should complete without error (skipping the step)
        runner.run(str(wf_path))
    finally:
        if wf_path.exists():
            wf_path.unlink()
