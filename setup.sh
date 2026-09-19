#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Clone tts if not exists
if [ ! -d "tts" ]; then
    git clone https://github.com/juanmirod/tts.git
fi

# Create venv (--system-site-packages so Termux's numpy is visible to tts)
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Install dependencies
pip install -r tts/requirements.txt
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env - add your OPENROUTER_API_KEY (or use the vault)"
fi

# Initialize episodes.json
if [ ! -f "episodes.json" ]; then
    echo "[]" > episodes.json
fi

# Create docs structure
mkdir -p docs/audio

echo "Setup complete! Run ./publish to create episodes."
