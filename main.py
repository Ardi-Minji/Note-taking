"""
Meeting Notes AI - Main CLI Interface
Entry point for the interactive CLI application.
"""

import os
import sys

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip
    pass


def validate_api_key():
    """Check if OpenAI API key is set in environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        print("\033[93m╔════════════════════════════════════════════════════════════╗")
        print("║                    DEMO MODE ENABLED                      ║")
        print("╚════════════════════════════════════════════════════════════╝\033[0m")
        print("\033[93mNo OpenAI API key found. Running in DEMO mode.\033[0m")
        print("Demo mode uses pattern matching instead of AI analysis.")
        print("\nTo enable AI-powered analysis:")
        print("  1. Get an API key from: https://platform.openai.com/api-keys")
        print("  2. Add to .env file: OPENAI_API_KEY=your-key-here")
        print("  3. Restart the application\n")
        return None
    return api_key


def display_help():
    """Display available commands and usage instructions."""
    help_text = """
\033[96m╔════════════════════════════════════════════════════════════╗
║           Meeting Notes AI - Available Commands           ║
╚════════════════════════════════════════════════════════════╝\033[0m

  📝 Paste transcript  → Analyze meeting and extract insights
  💾 save             → Save last analysis to markdown file
  📚 history          → Show summaries from current session
  ❓ help             → Show this help message
  🚪 q                → Quit application

\033[93mTo input a transcript:\033[0m
  1. Paste or type your meeting transcript
  2. Press Ctrl+D (Unix/Mac) or Ctrl+Z then Enter (Windows) when done
"""
    print(help_text)


def get_multiline_input():
    """Get multi-line input from user until EOF signal."""
    print("\n\033[93m📝 Paste your meeting transcript (Ctrl+D or Ctrl+Z when done):\033[0m")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    transcript = "\n".join(lines).strip()
    return transcript


def main():
    """Main entry point for the CLI application."""
    # Validate API key on startup (returns None if not found, enabling demo mode)
    api_key = validate_api_key()
    use_demo_mode = (api_key is None)
    
    # Display welcome message
    print("\033[96m")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                   Meeting Notes AI                        ║")
    print("║        Extract actionable insights from meetings          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    
    if use_demo_mode:
        print("\033[93m🎭 Running in DEMO MODE - Pattern matching analysis\033[0m\n")
    else:
        print("\033[92m🤖 AI Mode Active - Using OpenAI GPT-4o-mini\033[0m\n")
    
    display_help()
    
    # Import required modules
    from analyzer import analyze_transcript
    from formatter import format_terminal_output
    from file_handler import save_to_file, add_to_history, format_history_display
    
    # Store last analysis for save command
    last_analysis = None
    
    # Main interactive loop
    try:
        while True:
            print("\n\033[93m" + "="*60 + "\033[0m")
            print("\033[1mEnter command (or paste transcript):\033[0m", end=" ")
            
            try:
                command = input().strip().lower()
            except EOFError:
                print("\n\n\033[92mThank you for using Meeting Notes AI!\033[0m")
                break
            
            # Handle commands
            if command == 'q' or command == 'quit':
                print("\n\033[92mThank you for using Meeting Notes AI!\033[0m")
                break
                
            elif command == 'help' or command == '?':
                display_help()
                
            elif command == 'save':
                if last_analysis:
                    try:
                        filename = save_to_file(last_analysis)
                        print(f"\n\033[92m✓ Analysis saved to: {filename}\033[0m")
                    except Exception as e:
                        print(f"\n\033[91m✗ Error saving file: {str(e)}\033[0m")
                else:
                    print("\n\033[93m⚠ No analysis to save. Please analyze a transcript first.\033[0m")
                    
            elif command == 'history':
                print(format_history_display())
                
            elif command == '':
                # Empty input, prompt again
                continue
                
            else:
                # Treat as start of transcript input
                # Get the rest of the transcript
                transcript_lines = [command]
                transcript = get_multiline_input()
                
                if transcript:
                    transcript_lines.append(transcript)
                    full_transcript = '\n'.join(transcript_lines).strip()
                else:
                    full_transcript = command
                
                # Validate input
                if not full_transcript or full_transcript.isspace():
                    print("\n\033[91m✗ Error: Empty transcript. Please provide meeting content.\033[0m")
                    continue
                
                # Analyze transcript
                print("\n\033[96m⏳ Analyzing transcript...\033[0m")
                if use_demo_mode:
                    print("\033[93m(Using demo mode - pattern matching)\033[0m")
                try:
                    analysis = analyze_transcript(full_transcript, use_demo=use_demo_mode)
                    last_analysis = analysis
                    add_to_history(analysis)
                    
                    # Display results
                    print(format_terminal_output(analysis))
                    print("\n\033[92m✓ Analysis complete!\033[0m")
                    print("\033[93mTip: Type 'save' to save this analysis to a file\033[0m")
                    
                except Exception as e:
                    print(f"\n\033[91m✗ Error: {str(e)}\033[0m")
                    
    except KeyboardInterrupt:
        print("\n\n\033[92mThank you for using Meeting Notes AI!\033[0m")
    except Exception as e:
        print(f"\n\033[91m✗ Unexpected error: {str(e)}\033[0m")


if __name__ == "__main__":
    main()
