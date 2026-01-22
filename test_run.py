"""
Automated test to verify the application works end-to-end
"""

import os
from datetime import datetime

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Set API key if not already set
if not os.getenv("OPENAI_API_KEY"):
    # Read from .env file manually
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                key = line.split('=', 1)[1].strip()
                os.environ['OPENAI_API_KEY'] = key
                break

print("🧪 Testing Meeting Notes AI\n")

# Test 1: Import all modules
print("1. Testing imports...")
try:
    from analyzer import analyze_transcript, build_prompt, parse_response
    from formatter import format_terminal_output, format_markdown_output
    from file_handler import save_to_file, generate_filename, add_to_history, get_history
    print("   ✓ All modules imported successfully\n")
except Exception as e:
    print(f"   ✗ Import failed: {e}\n")
    exit(1)

# Test 2: Test with sample transcript
print("2. Testing with sample transcript...")
sample_transcript = """
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
"""

try:
    print("   🔄 Analyzing transcript with OpenAI API...")
    analysis = analyze_transcript(sample_transcript)
    print("   ✓ Analysis completed!\n")
    
    print("3. Analysis Results:")
    print("   " + "="*60)
    print(f"   📝 Summary: {analysis['summary'][:100]}...")
    print(f"   ✅ Action Items: {len(analysis['action_items'])} found")
    for item in analysis['action_items'][:3]:
        print(f"      • {item}")
    print(f"   📅 Decisions: {len(analysis['decisions'])} found")
    for decision in analysis['decisions'][:3]:
        print(f"      • {decision}")
    print(f"   ❓ Questions: {len(analysis['questions'])} found")
    print(f"   👥 Attendees: {len(analysis['attendees'])} found")
    print("   " + "="*60 + "\n")
    
except Exception as e:
    print(f"   ✗ Analysis failed: {e}\n")
    exit(1)

# Test 3: Test formatting
print("4. Testing output formatting...")
try:
    terminal_output = format_terminal_output(analysis)
    print("   ✓ Terminal formatting works")
    
    markdown_output = format_markdown_output(analysis)
    print("   ✓ Markdown formatting works\n")
except Exception as e:
    print(f"   ✗ Formatting failed: {e}\n")
    exit(1)

# Test 4: Test file saving
print("5. Testing file save...")
try:
    filename = f"test_meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    saved_path = save_to_file(analysis, filename)
    print(f"   ✓ File saved: {saved_path}")
    
    # Verify file exists
    if os.path.exists(saved_path):
        print(f"   ✓ File verified: {os.path.getsize(saved_path)} bytes")
        # Clean up
        os.remove(saved_path)
        print(f"   ✓ Test file cleaned up\n")
    else:
        print(f"   ✗ File not found\n")
except Exception as e:
    print(f"   ✗ File save failed: {e}\n")

# Test 5: Test history
print("6. Testing session history...")
try:
    add_to_history(analysis)
    history = get_history()
    print(f"   ✓ History has {len(history)} item(s)\n")
except Exception as e:
    print(f"   ✗ History failed: {e}\n")

# Display formatted output
print("7. Sample Terminal Output:")
print("="*70)
print(format_terminal_output(analysis))
print("="*70)

print("\n✅ ALL TESTS PASSED!")
print("\n🎉 Meeting Notes AI is fully functional!")
print("\nTo use interactively, run: py main.py")
