# Meeting Notes AI

A Python CLI tool that extracts actionable insights from meeting transcripts using AI.

## Features

- 📝 **Smart Analysis**: Automatically extracts summaries, action items, decisions, questions, and attendees
- 🎭 **Demo Mode**: Try it immediately without an API key using pattern matching
- 🤖 **AI Mode**: Connect OpenAI API for advanced AI-powered analysis
- ✅ **Action Items**: Identifies tasks with assigned persons when mentioned
- 💾 **Save to File**: Export analysis to timestamped markdown files
- 📚 **Session History**: Review all analyses from your current session
- 🎨 **Colored Output**: Easy-to-read terminal output with emojis and colors

## Quick Start (No API Key Required!)

The application works in **Demo Mode** by default - no API key needed to try it!

### Run Immediately
```bash
pip install python-dotenv
python main.py
```

That's it! The app will run in demo mode using pattern matching to analyze transcripts.

## Requirements

- Python 3.8 or higher
- OpenAI API key (optional - only needed for AI mode)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Optional**: For AI-powered analysis, set your OpenAI API key:

**Unix/Mac:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='your-api-key-here'
```

**Or add to .env file:**
```
OPENAI_API_KEY=your-api-key-here
```

## Usage Modes

### 🎭 Demo Mode (Default)
Works immediately without an API key. Uses pattern matching to extract:
- Attendees from "Name:" patterns
- Action items from keywords (will, should, need to, etc.)
- Decisions from keywords (decided, agreed, let's, etc.)
- Questions from "?" marks

### 🤖 AI Mode (Optional)
Connect an OpenAI API key for advanced AI-powered analysis with GPT-4o-mini:
- More accurate extraction
- Better context understanding
- Smarter summarization
- Handles complex transcripts

## Usage

Run the CLI tool:
```bash
python main.py
```

### Commands

- **Paste transcript**: Simply paste your meeting transcript and press `Ctrl+D` (Unix/Mac) or `Ctrl+Z` then Enter (Windows)
- **`save`**: Save the last analysis to a markdown file
- **`history`**: View summaries from your current session
- **`help`**: Show available commands
- **`q`**: Quit the application

### Example Workflow

1. Start the application: `python main.py`
2. Paste your meeting transcript
3. Press `Ctrl+D` (or `Ctrl+Z` + Enter on Windows)
4. Review the AI-generated analysis
5. Type `save` to export to a file
6. Continue with more transcripts or type `q` to quit

## Output Format

### Terminal Output
Colored, emoji-enhanced sections:
- 📝 Summary (3-5 sentences)
- ✅ Action Items
- 📅 Decisions Made
- ❓ Open Questions / Follow-ups
- 👥 Attendees

### File Output
Saved as: `meeting_notes_YYYY-MM-DD_HHMMSS.md`

Clean markdown format with all sections preserved.

## Example Transcript

```
Team standup meeting - January 22, 2026

John: Good morning everyone. Let's start with updates.

Sarah: I completed the user authentication module. It's ready for review.

Mike: Great! I'll review it by end of day. I'm currently working on the database migration.

John: Sounds good. Sarah, can you help Mike with the migration if he needs it?

Sarah: Absolutely, happy to help.

John: One more thing - we need to decide on the deployment strategy. Should we go with blue-green or canary?

Mike: I think canary would be safer for our use case.

Sarah: Agreed. Let's go with canary deployment.

John: Perfect. Mike, can you document the deployment plan by Friday?

Mike: Will do.

John: Any blockers or questions?

Sarah: Do we have access to the production environment yet?

John: Not yet, I'll follow up with DevOps today.
```

## Development

### Running Tests
```bash
pytest
```

### Project Structure
```
meeting-notes-ai/
├── main.py              # CLI entry point and main loop
├── analyzer.py          # OpenAI API integration
├── formatter.py         # Output formatting
├── file_handler.py      # File operations and history
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.


## Known Limitations

- **Session History**: History is only stored in memory and is cleared when the application exits
- **Input Method**: Currently only supports pasting text; no file upload functionality
- **API Dependency**: Requires active internet connection and valid OpenAI API key
- **Cost**: Each analysis uses OpenAI API credits (gpt-4o-mini is cost-efficient but not free)
- **Transcript Format**: Works best with clearly formatted transcripts with speaker names
- **Language**: Optimized for English transcripts
- **Output Directory**: Files are saved in the current working directory

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
Make sure you've set the API key in your environment. The setting only lasts for the current terminal session unless you add it to your shell profile.

### "Rate limit exceeded"
The tool will automatically retry with exponential backoff. If the issue persists, wait a few minutes before trying again.

### "Failed to connect to OpenAI API"
Check your internet connection and verify that you can access https://api.openai.com

### Multi-line input not working
- On Unix/Mac: Press `Ctrl+D` after pasting your transcript
- On Windows CMD: Press `Ctrl+Z` then `Enter`
- On Windows PowerShell: Press `Ctrl+Z` then `Enter`
