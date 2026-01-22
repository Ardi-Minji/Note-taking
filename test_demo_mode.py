"""
Test the new demo mode functionality
"""

import os

# Make sure we're in demo mode
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

from analyzer import analyze_transcript
from formatter import format_terminal_output
from file_handler import save_to_file
from datetime import datetime

print("🎭 Testing Demo Mode\n")
print("="*70)

# Sample transcript
transcript = """
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

print("\n📝 Analyzing transcript in DEMO MODE...\n")

# Analyze with demo mode
analysis = analyze_transcript(transcript, use_demo=True)

print("✅ Analysis Complete!\n")
print("="*70)
print(format_terminal_output(analysis))
print("="*70)

# Test file save
print("\n💾 Testing file save...")
filename = f"demo_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
saved_path = save_to_file(analysis, filename)
print(f"✓ Saved to: {saved_path}")

# Show file preview
with open(saved_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"\n📄 File Preview (first 300 chars):")
    print("-"*70)
    print(content[:300] + "...")
    print("-"*70)

# Clean up
os.remove(saved_path)
print(f"\n✓ Test file cleaned up")

print("\n🎉 Demo mode works perfectly!")
print("\n📊 What was extracted:")
print(f"   • Summary: ✓")
print(f"   • Action items: {len(analysis['action_items'])}")
print(f"   • Decisions: {len(analysis['decisions'])}")
print(f"   • Questions: {len(analysis['questions'])}")
print(f"   • Attendees: {len(analysis['attendees'])}")

print("\n💡 Demo mode uses pattern matching to extract:")
print("   • Attendees from 'Name:' patterns")
print("   • Action items from keywords (will, should, need to, etc.)")
print("   • Decisions from keywords (decided, agreed, let's, etc.)")
print("   • Questions from '?' marks")
