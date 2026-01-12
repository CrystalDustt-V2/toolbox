import pytest
from click.testing import CliRunner
from toolbox.cli import cli

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "ToolBox: A universal" in result.output

def test_fuzzy_matching():
    runner = CliRunner()
    # Try 'stat' which should fuzzy match to 'status'
    # FuzzyGroup raises UsageError (exit code 2) with a suggestion
    result = runner.invoke(cli, ["stat"])
    assert result.exit_code == 2
    assert "Did you mean 'status'?" in result.output

def test_workflow_group():
    runner = CliRunner()
    result = runner.invoke(cli, ["workflow", "--help"])
    assert result.exit_code == 0
    assert "run" in result.output
    assert "init" in result.output

def test_plugin_group():
    runner = CliRunner()
    result = runner.invoke(cli, ["plugins", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output
    assert "install" in result.output
