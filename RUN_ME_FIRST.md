# 🚀 Meeting Notes AI - Start Here!

## ⚡ Instant Demo (30 seconds)

No setup needed! The app works immediately in demo mode.

### Step 1: Install one dependency (if needed)
```bash
py -m pip install python-dotenv
```

### Step 2: Run the app
```bash
py main.py
```

**Note:** Use `py` instead of `python` on Windows!

### Step 3: Try it!
When prompted, paste this example:

```
John: Let's discuss the project timeline.
Sarah: I'll finish the design by Friday.
Mike: I need help with the database.
John: Sarah, can you help Mike?
Sarah: Sure, I'll help after I finish the design.
John: Great! Let's meet again next week.
```

Then press **Ctrl+Z** and **Enter** (Windows) or **Ctrl+D** (Mac/Linux)

## 🎉 That's It!

You'll see:
- 📝 Summary of the meeting
- ✅ Action items extracted
- 📅 Decisions made
- ❓ Questions raised
- 👥 Attendees identified

## 💡 What Just Happened?

The app ran in **Demo Mode** using pattern matching. No AI, no API key, no cost!

## 🤖 Want AI-Powered Analysis?

Demo mode is great for testing, but AI mode is smarter:

1. Get an API key: https://platform.openai.com/api-keys
2. Edit `.env` file and replace `your-api-key-here` with your actual key
3. Restart the app

AI mode uses GPT-4o-mini for better analysis (costs a few cents per transcript).

## 📚 Learn More

- **README.md** - Full documentation
- **QUICKSTART.md** - Detailed guide
- **example_transcript.txt** - Sample transcript to try

## 🎯 Quick Commands

Once the app is running:
- Type `help` - Show commands
- Type `save` - Save analysis to file
- Type `history` - View session history
- Type `q` - Quit

## ✨ Features

✅ Works immediately (demo mode)  
✅ No API key required to start  
✅ Extracts action items automatically  
✅ Identifies attendees  
✅ Saves to markdown files  
✅ Colored terminal output  
✅ Session history  
✅ Optional AI upgrade  

## 🆘 Troubleshooting

**"pip not found"**
- Install Python from python.org
- Make sure "Add to PATH" is checked during installation

**"python not found"**
- Try `py main.py` instead of `python main.py`

**App won't start**
- Make sure you're in the project directory
- Run: `pip install python-dotenv`

## 🎊 You're Ready!

Just run `python main.py` and start analyzing meetings!
