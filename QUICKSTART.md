# Quick Start Guide - Meeting Notes AI

## Instant Start (No API Key Needed!)

The app works immediately in **Demo Mode** - no setup required!

### 1. Install (30 seconds)
```bash
pip install python-dotenv
```

### 2. Run
```bash
python main.py
```

That's it! The app is now running in demo mode.

## Try It Now

1. **Start the app**: `python main.py`

2. **Paste this example**:

```
Team standup - January 22, 2026

John: Good morning. Let's start with updates.

Sarah: I completed the authentication module. Ready for review.

Mike: I'll review it today. Working on database migration.

John: Sarah, can you help Mike if needed?

Sarah: Absolutely.

John: We need to decide on deployment. Blue-green or canary?

Mike: Canary would be safer.

Sarah: Agreed.

John: Mike, document the plan by Friday?

Mike: Will do.

John: Any blockers?

Sarah: Do we have prod access yet?

John: I'll follow up with DevOps.
```

3. **Press Ctrl+D** (Unix/Mac) or **Ctrl+Z then Enter** (Windows)

4. **View the analysis** - You'll see:
   - 📝 Summary
   - ✅ Action Items
   - 📅 Decisions
   - ❓ Questions
   - 👥 Attendees

5. **Save the results**: Type `save` and press Enter

6. **View history**: Type `history` to see past analyses

7. **Quit**: Type `q` and press Enter

## Commands

- **Paste transcript** → Get analysis (demo or AI mode)
- **`save`** → Save last analysis to markdown file
- **`history`** → Show session summaries
- **`help`** → Show commands
- **`q`** → Quit

## Two Modes

### 🎭 Demo Mode (Default - No API Key)
- Works immediately
- Uses pattern matching
- Free to use
- Good for testing

### 🤖 AI Mode (Optional - Requires API Key)
- More accurate
- Better understanding
- Costs a few cents per analysis
- Uses GPT-4o-mini

## Upgrade to AI Mode (Optional)

Want better analysis? Add an OpenAI API key:

1. Get key from: https://platform.openai.com/api-keys
2. Add to `.env` file:
   ```
   OPENAI_API_KEY=your-actual-key-here
   ```
3. Restart the app

## Tips

- Demo mode is perfect for trying the app
- Demo mode extracts attendees, actions, decisions, and questions
- AI mode provides smarter summaries and better context understanding
- Both modes save to markdown files
- History works in both modes

## Troubleshooting

**"OPENAI_API_KEY not set"**
- Make sure you set the environment variable in the same terminal where you run the app

**"Rate limit exceeded"**
- Wait a minute and try again
- The tool will automatically retry with backoff

**Multi-line input not working**
- Make sure to press Ctrl+D (or Ctrl+Z + Enter on Windows) after pasting

## Running Tests

```bash
# Unit tests
pytest test_analyzer.py test_formatter.py test_file_handler.py -v

# Property-based tests
pytest test_properties.py -v

# All tests
pytest -v
```

## Security Note

⚠️ **Never commit or share your API key!**
- Don't add it to version control
- Don't share it in chat or messages
- Revoke and regenerate if accidentally exposed
