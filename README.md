# Podcast CLI Uploader

A TDD-built CLI tool to convert text to speech and publish it as a podcast on GitHub Pages.

## Features

- Converts text to speech using `juanmirod/tts` (OpenAI `gpt-4o-mini-tts`).
- Supports input from files or stdin pipes.
- Interactive or non-interactive metadata entry.
- Automatically generates a modern HTML homepage and a valid RSS feed.
- Orchestrates git operations (add, commit, push) to publish to GitHub Pages.
- Termux compatible.

## Setup

1. Clone this repository.
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Add your OpenAI API key to the `.env` file created.
4. Configure your podcast details in `podcast.json`.

## Usage

### Basic Usage

```bash
./publish input.txt
```

### Using Pipes

```bash
cat article.txt | ./publish --title "My Episode" --voice coral
```

### Command Line Options

```bash
./publish -h
```

Options:
- `-t, --title`: Episode title.
- `-d, --description`: Episode description.
- `-v, --voice`: Choice of voice (alloy, ash, coral, echo, fable, onyx, nova, sage, shimmer).
- `--no-push`: Skip git push.
- `--no-commit`: Skip git commit and push.

## Development

### Running Tests

```bash
source venv/bin/activate
pytest
```

### Running the Website Locally

To preview the generated website before pushing to GitHub Pages:

```bash
# From the project root, serve the docs folder
python -m http.server 8000 -d docs
```

Then open http://localhost:8000 in your browser.

Alternatively, if you have Node.js installed:

```bash
npx serve docs
```

## GitHub Pages

Enable GitHub Pages in your repository settings:
- Source: Deploy from a branch
- Branch: `main` (or `master`)
- Folder: `/docs`
