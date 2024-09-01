import subprocess
import pytest

def run_cli(args):
    result = subprocess.run(['python', 'annote.py'] + args, capture_output=True, text=True)
    return result

def test_print_info():
    result = run_cli(['annote'])
    assert result.returncode == 0
    assert "Annote CLI App" in result.stdout

def test_create_note():
    result = run_cli(['note', 'This is a test note'])
    assert result.returncode == 0
    assert "Creating note: This is a test note" in result.stdout

def test_query_entries_default():
    result = run_cli(['query'])
    assert result.returncode == 0
    assert "Showing the latest 50 entries" in result.stdout

def test_query_entries_with_limit():
    result = run_cli(['query', '-l', '100'])
    assert result.returncode == 0
    assert "Showing the latest 100 entries" in result.stdout

def test_query_entries_with_search():
    result = run_cli(['query', '-s', 'search_term'])
    assert result.returncode == 0
    assert "Filtering by: search_term" in result.stdout

def test_query_generations():
    result = run_cli(['query', '-g'])
    assert result.returncode == 0
    assert "Showing the latest 50 generations" in result.stdout

def test_query_generations_with_limit():
    result = run_cli(['query', '-g', '-l', '100'])
    assert result.returncode == 0
    assert "Showing the latest 100 generations" in result.stdout

def test_query_tasks():
    result = run_cli(['query', '-t'])
    assert result.returncode == 0
    assert "Showing the latest 50 focused tasks" in result.stdout

def test_query_tasks_with_limit():
    result = run_cli(['query', '-t', '-l', '100'])
    assert result.returncode == 0
    assert "Showing the latest 100 focused tasks" in result.stdout

def test_query_tasks_unfocused():
    result = run_cli(['query', '-t', '-f', 'false'])
    assert result.returncode == 0
    assert "Showing the latest 50 unfocused tasks" in result.stdout

def test_delete_flush_annotations_cancel():
    # Simulating user not confirming the flush operation
    result = subprocess.run(['python', 'annote.py', 'delete', '--flush-annotations'], input="no\n", capture_output=True, text=True)
    assert result.returncode == 0
    assert "Operation canceled." in result.stdout

def test_delete_flush_annotations_confirm():
    # Simulating user confirming the flush operation
    result = subprocess.run(['python', 'annote.py', 'delete', '--flush-annotations'], input="yes\n", capture_output=True, text=True)
    assert result.returncode == 0
    assert "Flushing annotations..." in result.stdout

def test_run_command():
    result = run_cli(['command', 'echo Hello'])
    assert result.returncode == 0
    assert "Running command: echo Hello" in result.stdout
