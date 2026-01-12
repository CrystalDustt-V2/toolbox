import pytest
import os
from pathlib import Path
from click.testing import CliRunner
from toolbox.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Hello World", encoding="utf-8")
    return f

def test_file_hash(runner, temp_file):
    # SHA256 of "Hello World" is a591a...
    result = runner.invoke(cli, ["file", "hash", str(temp_file), "--algorithm", "sha256"])
    assert result.exit_code == 0
    assert "SHA256:" in result.output
    assert "a591a" in result.output.lower()

def test_file_info(runner, temp_file):
    result = runner.invoke(cli, ["file", "info", str(temp_file)])
    assert result.exit_code == 0
    # Rich table output might look different, check for presence of name and size
    assert temp_file.name in result.output
    assert "Size" in result.output
    assert "11 bytes" in result.output

def test_file_rename(runner, temp_file):
    new_name = temp_file.parent / "renamed.txt"
    result = runner.invoke(cli, ["file", "rename", str(temp_file), str(new_name)])
    assert result.exit_code == 0
    assert not temp_file.exists()
    assert new_name.exists()
    assert new_name.read_text() == "Hello World"

def test_file_batch_rename(runner, tmp_path):
    # Create a few files
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.txt").write_text("2")
    (tmp_path / "image.jpg").write_text("3")
    
    # Prefix only .txt files
    result = runner.invoke(cli, ["file", "batch-rename", str(tmp_path), "--prefix", "pre_", "--ext", ".txt"])
    assert result.exit_code == 0
    assert (tmp_path / "pre_file1.txt").exists()
    assert (tmp_path / "pre_file2.txt").exists()
    assert (tmp_path / "image.jpg").exists()
    assert not (tmp_path / "file1.txt").exists()

def test_file_encryption(runner, temp_file):
    # Test encryption
    password = "testpassword"
    enc_file = f"{temp_file}.enc"
    result = runner.invoke(cli, ["file", "encrypt", str(temp_file), "-p", password])
    assert result.exit_code == 0
    assert os.path.exists(enc_file)
    
    # Test decryption
    dec_file = f"{temp_file}.dec"
    result = runner.invoke(cli, ["file", "decrypt", enc_file, "-p", password, "-o", dec_file])
    assert result.exit_code == 0
    assert os.path.exists(dec_file)
    with open(dec_file, "r") as f:
        assert f.read() == "Hello World"

def test_file_shred(runner, temp_file):
    result = runner.invoke(cli, ["file", "shred", str(temp_file), "--passes", "1"])
    assert result.exit_code == 0
    assert not temp_file.exists()
