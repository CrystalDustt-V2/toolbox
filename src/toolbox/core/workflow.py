import yaml
import click
import shlex
import os
import re
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console

console = Console()

class WorkflowError(Exception):
    """Base class for workflow related errors."""
    pass

class WorkflowRunner:
    def __init__(self, cli_group: click.Group):
        self.cli_group = cli_group
        self.variables: Dict[str, str] = {}

    def _substitute_vars(self, text: str) -> str:
        """Substitute ${VAR} or $VAR with values from self.variables or environment."""
        def replace(match):
            var_name = match.group(1) or match.group(2)
            # Priority: Workflow Variables > Environment Variables
            val = self.variables.get(var_name, os.environ.get(var_name, match.group(0)))
            return str(val)
        
        # Matches ${VAR} or $VAR
        pattern = r"\$\{(\w+)\}|\$(\w+)"
        return re.sub(pattern, replace, text)

    def _execute_step(self, step: Dict[str, Any], step_index: int) -> bool:
        """Execute a single workflow step. Returns True if successful."""
        step_name = step.get("name", f"Step {step_index + 1}")
        
        # Check condition if present
        condition = step.get("if")
        if condition:
            condition = self._substitute_vars(condition)
            if condition.lower() in ["false", "0", "no", "none", ""]:
                console.print(f"[dim]Skipping {step_name} (condition '{condition}' is false)[/dim]")
                return True
        
        command_str = step.get("command")
        if not command_str:
            console.print(f"[red]Error: Step '{step_name}' has no command.[/red]")
            return False

        command_str = self._substitute_vars(command_str)
        console.print(f"\n[bold blue]>>> Executing {step_name}...[/bold blue]")
        console.print(f"[dim]Command: {command_str}[/dim]")

        try:
            args = shlex.split(command_str)
            self.cli_group.main(args=args, standalone_mode=False)
            console.print(f"[green]✓ {step_name} completed successfully.[/green]")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ {step_name} failed:[/bold red] {str(e)}")
            if step.get("continue_on_error", False):
                return True
            return False

    def run(self, workflow_path: str, overrides: Dict[str, str] = None):
        path = Path(workflow_path)
        if not path.exists():
            raise WorkflowError(f"Workflow file not found: {workflow_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise WorkflowError(f"Failed to parse workflow YAML: {str(e)}")

        # Initialize variables
        self.variables = data.get("vars", {})
        if overrides:
            self.variables.update(overrides)

        workflow_name = data.get("name", "Unnamed Workflow")
        steps = data.get("steps", [])
        parallel_mode = data.get("parallel", False)

        if not steps:
            console.print("[yellow]Warning: No steps found in workflow.[/yellow]")
            return

        console.print(f"[bold green]Starting Workflow:[/bold green] {workflow_name} {'(Parallel Mode)' if parallel_mode else ''}")
        
        if parallel_mode:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Map steps to future executions
                futures = {executor.submit(self._execute_step, step, i): step for i, step in enumerate(steps)}
                for future in concurrent.futures.as_completed(futures):
                    step = futures[future]
                    if not future.result() and not step.get("continue_on_error", False):
                        console.print(f"[bold red]Workflow aborted due to failure in parallel step.[/bold red]")
                        executor.shutdown(wait=False, cancel_futures=True)
                        raise WorkflowError("Parallel workflow execution failed.")
        else:
            for i, step in enumerate(steps):
                success = self._execute_step(step, i)
                if not success:
                    raise WorkflowError(f"Workflow aborted at step '{step.get('name', i+1)}'")

        console.print(f"\n[bold green]Workflow '{workflow_name}' completed![/bold green]")
