"""
Quick test script to verify the application works
"""

import os
import sys

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ .env file loaded")
except ImportError:
    print("⚠ python-dotenv not installed, trying environment variable...")

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("✗ OPENAI_API_KEY not found!")
    sys.exit(1)
else:
    print(f"✓ API key found (starts with: {api_key[:10]}...)")

# Test imports
try:
    from analyzer import build_prompt, parse_response
    print("✓ analyzer module imported")
except Exception as e:
    print(f"✗ Failed to import analyzer: {e}")
    sys.exit(1)

try:
    from formatter import format_terminal_output, format_markdown_output
    print("✓ formatter module imported")
except Exception as e:
    print(f"✗ Failed to import formatter: {e}")
    sys.exit(1)

try:
    from file_handler import generate_filename, save_to_file
    print("✓ file_handler module imported")
except Exception as e:
    print(f"✗ Failed to import file_handler: {e}")
    sys.exit(1)

# Test basic functionality
print("\n--- Testing Basic Functions ---")

# Test prompt building
transcript = "Test meeting with John and Sarah discussing the project."
prompt = build_prompt(transcript)
print(f"✓ Prompt built ({len(prompt)} characters)")

# Test filename generation
filename = generate_filename()
print(f"✓ Filename generated: {filename}")

# Test response parsing
test_response = """
SUMMARY:
This is a test summary of the meeting.

ACTION ITEMS:
- John to complete the report
- Sarah to review the code

DECISIONS MADE:
- Approved the new design

OPEN QUESTIONS:
- When is the deadline?

ATTENDEES:
- John
- Sarah
"""

result = parse_response(test_response)
print(f"✓ Response parsed successfully")
print(f"  - Summary: {result['summary'][:50]}...")
print(f"  - Action items: {len(result['action_items'])}")
print(f"  - Decisions: {len(result['decisions'])}")

# Test formatting
output = format_terminal_output(result)
print(f"✓ Terminal output formatted ({len(output)} characters)")

markdown = format_markdown_output(result)
print(f"✓ Markdown output formatted ({len(markdown)} characters)")

print("\n✅ All basic tests passed!")
print("\nNow testing with OpenAI API...")

# Test OpenAI API
try:
    from openai import OpenAI
    print("✓ OpenAI library imported")
    
    client = OpenAI(api_key=api_key)
    print("✓ OpenAI client created")
    
    # Make a simple test call
    print("\n🔄 Making test API call...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'Hello, Meeting Notes AI is working!' in exactly those words."}
        ],
        max_tokens=50
    )
    
    result_text = response.choices[0].message.content
    print(f"✓ API call successful!")
    print(f"  Response: {result_text}")
    
    print("\n🎉 SUCCESS! The application is fully functional!")
    print("\nYou can now run: py main.py")
    
except ImportError as e:
    print(f"✗ OpenAI library not installed: {e}")
    print("\nPlease install: pip install openai python-dotenv")
except Exception as e:
    print(f"✗ API call failed: {e}")
    print("\nThis might be due to:")
    print("  1. Invalid API key")
    print("  2. Network connection issues")
    print("  3. OpenAI API issues")
