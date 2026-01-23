---
name: Podcast CLI Uploader
overview: Create a Python CLI tool using TDD that uses juanmirod/tts for text-to-speech conversion, then orchestrates publishing episodes to a GitHub Pages podcast site with an RSS feed.
todos:
  - id: setup-project
    content: Create project structure, setup.sh, requirements.txt (with pytest), .gitignore, .env.example
    status: completed
  - id: tdd-input-handling
    content: "TDD cycle: Input handling - read from file or stdin"
    status: completed
  - id: tdd-episode-metadata
    content: "TDD cycle: Episode metadata - read/write episodes.json, generate GUID, slugify"
    status: in_progress
  - id: tdd-site-generation
    content: "TDD cycle: Site generation - render feed.xml and index.html from templates"
    status: pending
  - id: tdd-tts-integration
    content: "TDD cycle: TTS integration - call tts module, move audio file"
    status: pending
  - id: tdd-git-operations
    content: "TDD cycle: Git operations - add, commit, push"
    status: pending
  - id: tdd-cli-integration
    content: "TDD cycle: CLI integration - argparse, interactive prompts, main flow"
    status: pending
  - id: wrapper-and-docs
    content: Create publish wrapper script, templates, docs/ structure, README.md
    status: pending
isProject: false
---

# Podcast CLI Uploader (TDD)

## Project Structure

```
podcast-uploader/
├── publish                 # Wrapper script (activates venv, runs CLI)
├── publish.py              # Main CLI entry point
├── podcast/                # Python package
│   ├── __init__.py
│   ├── input_handler.py    # Read from file or stdin
│   ├── episodes.py         # Episode metadata management
│   ├── site_generator.py   # Generate feed.xml and index.html
│   ├── tts_runner.py       # TTS subprocess wrapper
│   └── git_ops.py          # Git add/commit/push
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_input_handler.py
│   ├── test_episodes.py
│   ├── test_site_generator.py
│   ├── test_tts_runner.py
│   └── test_git_ops.py
├── templates/              # Jinja2 templates
│   ├── index.html.j2
│   └── feed.xml.j2
├── setup.sh                # One-time setup
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Test dependencies (pytest)
├── .env.example
├── .gitignore
├── README.md
├── podcast.json            # Podcast metadata
├── episodes.json           # Episode list
└── docs/                   # GitHub Pages output
    ├── index.html
    ├── feed.xml
    ├── style.css
    └── audio/
```

## TDD Workflow

Each feature follows the Red-Green-Refactor cycle:

```
1. RED:    Write a failing test
2. GREEN:  Write minimum code to pass
3. REFACTOR: Clean up, keep tests green
4. COMMIT: git commit with descriptive message
```

## TDD Cycles

### Cycle 1: Input Handling (`podcast/input_handler.py`)

**Tests to write:**

```python
# test_input_handler.py
def test_read_from_file():
    """Should read text content from a file path"""

def test_read_from_file_not_found():
    """Should raise error if file doesn't exist"""

def test_read_from_stdin(monkeypatch):
    """Should read from stdin when no file provided and stdin has data"""

def test_error_when_no_input():
    """Should raise error when no file and stdin is a tty"""
```

### Cycle 2: Episode Metadata (`podcast/episodes.py`)

**Tests to write:**

```python
# test_episodes.py
def test_load_episodes_empty():
    """Should return empty list from empty episodes.json"""

def test_load_episodes_with_data():
    """Should return list of episodes from episodes.json"""

def test_save_episodes():
    """Should write episodes list to episodes.json"""

def test_create_episode():
    """Should create episode dict with title, description, date, guid, filename"""

def test_generate_filename():
    """Should generate YYYYMMDD-HHMMSS-slug.mp3 format"""

def test_add_episode():
    """Should prepend new episode to list"""
```

### Cycle 3: Site Generation (`podcast/site_generator.py`)

**Tests to write:**

```python
# test_site_generator.py
def test_render_feed_xml():
    """Should render valid RSS XML with episodes"""

def test_render_feed_xml_empty():
    """Should render valid RSS XML with no episodes"""

def test_render_index_html():
    """Should render HTML page with episode list"""

def test_generate_site():
    """Should write feed.xml and index.html to docs/"""

def test_rfc2822_date():
    """Should format datetime as RFC 2822 string"""

def test_format_duration():
    """Should format seconds as HH:MM:SS or MM:SS"""
```

### Cycle 4: TTS Integration (`podcast/tts_runner.py`)

**Tests to write:**

```python
# test_tts_runner.py
def test_run_tts_success(mocker):
    """Should call tts module and return output path"""

def test_run_tts_with_voice(mocker):
    """Should pass voice argument to tts"""

def test_move_audio_to_docs():
    """Should move mp3 file to docs/audio/ with new name"""

def test_get_audio_duration():
    """Should return duration in seconds from mp3 file"""

def test_get_audio_filesize():
    """Should return file size in bytes"""
```

### Cycle 5: Git Operations (`podcast/git_ops.py`)

**Tests to write:**

```python
# test_git_ops.py
def test_git_add(mocker):
    """Should run git add with correct paths"""

def test_git_commit(mocker):
    """Should run git commit with message"""

def test_git_push(mocker):
    """Should run git push"""

def test_commit_episode(mocker):
    """Should add, commit with episode title, and push"""

def test_commit_episode_no_push(mocker):
    """Should add and commit but skip push when flag set"""
```

### Cycle 6: CLI Integration (`publish.py`)

**Tests to write:**

```python
# test_cli.py
def test_parse_args_with_file():
    """Should parse file argument"""

def test_parse_args_with_options():
    """Should parse --title, --voice, --description"""

def test_parse_args_no_push():
    """Should parse --no-push flag"""

def test_main_flow(mocker):
    """Should orchestrate all steps in correct order"""

def test_interactive_prompt_title(mocker):
    """Should prompt for title if not provided"""
```

## Dependencies

### `requirements.txt` (Runtime - Pure Python for Termux)

```
jinja2>=3.0.0
python-slugify>=8.0
mutagen>=1.47.0
python-dotenv>=1.0.0
```

### `requirements-dev.txt` (Testing)

```
-r requirements.txt
pytest>=7.0.0
pytest-mock>=3.0.0
```

## Wrapper Script (`publish`)

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/publish.py" "$@"
```

## CLI Usage

```bash
# From file
./publish input.txt

# From stdin (pipe support)
cat article.txt | ./publish
echo "Hello world" | ./publish

# With command-line options (non-interactive)
./publish --title "Episode 1" --voice coral input.txt
cat text.txt | ./publish -t "Episode 1" -d "Description"

# Skip git operations
./publish --no-push input.txt
./publish --no-commit input.txt
```

## Running Tests

```bash
# Activate venv
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=podcast

# Run specific test file
pytest tests/test_episodes.py

# Run in watch mode (with pytest-watch)
ptw
```

## Commit Strategy

One commit per TDD cycle after all steps are complete (red, green, refactor):

```
feat(<module>): <what the feature does>

<Description of the change and why>
```

Example commit history:

```
feat(cli): add CLI entry point with argparse and interactive prompts

Implements argument parsing for file input, --title, --voice, --description,
--no-push, and --no-commit flags. Falls back to interactive prompts when
options not provided via command line.

feat(git): add git operations for committing episodes

Implements git add, commit, and push functionality with optional skip flags.
Mocks subprocess calls in tests.

feat(tts): add TTS runner with audio file handling

Wraps juanmirod/tts module, moves output to docs/audio/ with timestamped
filename, extracts duration and filesize using mutagen.

feat(site): add site generator for feed.xml and index.html

Uses Jinja2 templates to render podcast RSS feed and HTML homepage.
Includes RFC 2822 date formatting and duration formatting helpers.

feat(episodes): add episode metadata management

Handles loading/saving episodes.json, creating episode dicts with GUID,
generating slugified filenames with timestamps.

feat(input): add input handler for file and stdin

Reads text from file path or stdin pipe. Raises error when no input provided.
```