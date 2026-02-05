#!/bin/bash

# EduBot startup script

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for BOT_TOKEN
if [ -z "$BOT_TOKEN" ]; then
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
fi

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ BOT_TOKEN not set!"
    echo "Set it with: export BOT_TOKEN='your_token_here'"
    exit 1
fi

# Run the bot
echo "🤖 Starting EduBot..."
python src/bot.py
