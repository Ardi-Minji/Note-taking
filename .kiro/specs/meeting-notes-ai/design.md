# Meeting Notes AI - Design Document

## Architecture Overview

The application follows a simple modular architecture with clear separation of concerns:

```
meeting-notes-ai/
├── main.py              # Entry point and CLI loop
├── analyzer.py          # AI analysis logic
├── formatter.py         # Output formatting
├── file_handler.py      # File operations
└── requirements.txt     # Dependencies
```

## Component Design

### 1. Main CLI Loop (main.py)
**Responsibility:** Orchestrate user interaction and command routing

**Key Functions:**
- `main()`: Entry point, initializes session and runs interactive loop
- `get_multiline_input()`: Handles multi-line transcript input
- `display_help()`: Shows available commands
- `validate_api_key()`: Checks for OPENAI_API_KEY environment variable

**Flow:**
1. Validate API key on startup
2. Display welcome message and instructions
3. Enter interactive loop:
   - Prompt for input
   - Route to appropriate handler (analyze, save, history, quit)
   - Display results
   - Repeat

### 2. AI Analyzer (analyzer.py)
**Responsibility:** Interface with OpenAI API and parse responses

**Key Functions:**
- `analyze_transcript(transcript: str) -> dict`: Main analysis function
- `build_prompt(transcript: str) -> str`: Constructs the AI prompt
- `parse_response(response: str) -> dict`: Parses AI output into structured data

**AI Prompt Structure:**
```
Analyze the following meeting transcript and extract:
1. Summary (3-5 sentences)
2. Action Items (with assigned person if mentioned)
3. Decisions Made
4. Open Questions / Follow-ups
5. Attendees (if mentioned)

Format your response as structured sections.
```

**Return Format:**
```python
{
    'summary': str,
    'action_items': list[str],
    'decisions': list[str],
    'questions': list[str],
    'attendees': list[str],
    'timestamp': datetime
}
```

### 3. Output Formatter (formatter.py)
**Responsibility:** Format analysis results for terminal and file output

**Key Functions:**
- `format_terminal_output(analysis: dict) -> str`: Colored terminal output with emojis
- `format_markdown_output(analysis: dict) -> str`: Clean markdown for file export

**Terminal Output Format:**
```
📝 SUMMARY
[colored text with summary]

✅ ACTION ITEMS
• [action item 1]
• [action item 2]

📅 DECISIONS MADE
• [decision 1]

❓ OPEN QUESTIONS
• [question 1]

👥 ATTENDEES
• [attendee 1]
```

**Color Scheme:**
- Headers: Cyan/Bold
- Content: White
- Success messages: Green
- Error messages: Red
- Prompts: Yellow

### 4. File Handler (file_handler.py)
**Responsibility:** Manage file operations and session history

**Key Functions:**
- `save_to_file(analysis: dict, filename: str = None) -> str`: Save analysis to markdown
- `generate_filename() -> str`: Create timestamped filename
- `add_to_history(analysis: dict)`: Store analysis in session history
- `get_history() -> list[dict]`: Retrieve session history
- `format_history_display() -> str`: Format history for terminal display

**Session History:**
- Stored in memory (list of analysis dicts)
- Cleared on application exit
- Displays summary + timestamp for each entry

## Data Flow

```
User Input (Transcript)
    ↓
Main CLI Loop
    ↓
Analyzer (OpenAI API)
    ↓
Structured Analysis Dict
    ↓
├─→ Formatter (Terminal) → Display
├─→ File Handler (History) → Store
└─→ File Handler (Save) → Markdown File
```

## Error Handling Strategy

### API Errors
- Missing API key: Exit with clear error message
- API call failure: Display error, allow retry
- Rate limiting: Inform user, suggest waiting

### Input Errors
- Empty transcript: Prompt for valid input
- Invalid command: Show help message

### File Errors
- Write permission issues: Display error, suggest alternative location
- Disk space issues: Inform user

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required, OpenAI API key

### Constants
```python
MODEL = "gpt-4o-mini"
MAX_TOKENS = 1000
TEMPERATURE = 0.7
OUTPUT_DIR = "./meeting_notes"
```

## Testing Strategy

### Unit Tests
- Test prompt building
- Test response parsing
- Test filename generation
- Test markdown formatting

### Integration Tests
- Test full analysis flow with mock API
- Test file save operations
- Test history management

### Manual Testing
- Test with various transcript formats
- Test error scenarios (no API key, network issues)
- Test multi-line input handling
- Verify colored output in different terminals

## Correctness Properties

### Property 1.1: Input Validation
**Description:** All user inputs must be validated before processing
**Test Strategy:** Property-based test with various input types (empty, whitespace-only, very long strings)

### Property 1.2: API Key Validation
**Description:** Application must not proceed without valid API key
**Test Strategy:** Unit test checking startup behavior with missing/invalid keys

### Property 2.1: Output Completeness
**Description:** Analysis output must contain all required sections
**Test Strategy:** Property-based test verifying all keys present in analysis dict

### Property 2.2: Output Structure
**Description:** Each section must be properly formatted with correct emoji and structure
**Test Strategy:** Unit tests for formatter functions

### Property 3.1: Filename Uniqueness
**Description:** Generated filenames must be unique and follow the specified pattern
**Test Strategy:** Property-based test generating multiple filenames in sequence

### Property 3.2: File Content Integrity
**Description:** Saved markdown files must contain all analysis data
**Test Strategy:** Integration test: save → read → verify content

### Property 4.1: History Persistence
**Description:** Session history must retain all analyses until session ends
**Test Strategy:** Unit test adding multiple items and verifying retrieval

### Property 5.1: Command Recognition
**Description:** CLI must correctly identify and route all valid commands
**Test Strategy:** Unit tests for each command (save, history, q)

### Property 6.1: API Error Handling
**Description:** All API errors must be caught and handled gracefully
**Test Strategy:** Integration tests with mocked API failures

## Implementation Notes

### Multi-line Input Handling
Use one of these approaches:
1. Read until EOF (Ctrl+D on Unix, Ctrl+Z on Windows)
2. Read until empty line
3. Use special delimiter (e.g., "END")

Recommended: EOF approach for simplicity

### Colored Output
Use ANSI escape codes or simple library like `colorama` (if allowed as minimal dependency)
If no external deps allowed, implement basic ANSI codes directly

### OpenAI API Integration
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
```

## Future Enhancements (Out of Scope)
- Clipboard integration for output
- Support for reading transcript files directly
- Export to other formats (PDF, JSON)
- Integration with calendar apps
- Multi-session history persistence
