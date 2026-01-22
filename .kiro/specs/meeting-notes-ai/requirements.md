# Meeting Notes AI - Requirements

## Overview
A Python CLI tool that analyzes meeting transcripts using AI to extract actionable insights including summaries, action items, decisions, open questions, and attendees.

## User Stories

### 1. As a user, I want to input meeting transcripts so that I can get AI-powered analysis
**Acceptance Criteria:**
- 1.1 The CLI accepts multi-line text input for meeting transcripts
- 1.2 The CLI provides clear instructions on how to input transcripts
- 1.3 The CLI handles empty or invalid input gracefully with error messages
- 1.4 Users can signal end of input (e.g., EOF or special command)

### 2. As a user, I want to see structured analysis of my meeting transcript
**Acceptance Criteria:**
- 2.1 The output includes a summary section (3-5 sentences)
- 2.2 The output includes action items with assigned persons when mentioned
- 2.3 The output includes decisions made during the meeting
- 2.4 The output includes open questions and follow-ups
- 2.5 The output includes attendees list when mentioned in transcript
- 2.6 Each section is clearly labeled with emoji icons for visual clarity
- 2.7 Output uses colored terminal text for better readability

### 3. As a user, I want to save analysis results to a file
**Acceptance Criteria:**
- 3.1 Users can save the last analysis output using a 'save' command
- 3.2 Files are saved in markdown format
- 3.3 Filenames follow the pattern: meeting_notes_YYYY-MM-DD_HHMMSS.md
- 3.4 The CLI confirms successful file save with the filename
- 3.5 The CLI handles file write errors gracefully

### 4. As a user, I want to view my session history
**Acceptance Criteria:**
- 4.1 Users can view past meeting summaries from the current session using 'history' command
- 4.2 History displays at minimum the summary section of each analysis
- 4.3 History includes timestamps for each meeting analysis
- 4.4 History is cleared when the CLI session ends

### 5. As a user, I want an interactive CLI experience
**Acceptance Criteria:**
- 5.1 The CLI runs in an interactive loop
- 5.2 Users can analyze multiple transcripts in one session
- 5.3 Users can quit the application using 'q' command
- 5.4 The CLI provides helpful prompts and feedback
- 5.5 The CLI displays available commands

### 6. As a user, I want the tool to use OpenAI API efficiently
**Acceptance Criteria:**
- 6.1 The tool uses gpt-4o-mini model for cost efficiency
- 6.2 The tool reads OpenAI API key from OPENAI_API_KEY environment variable
- 6.3 The tool validates API key presence before making requests
- 6.4 The tool handles API errors gracefully with user-friendly messages
- 6.5 The tool provides feedback during API calls (e.g., "Analyzing...")

## Technical Constraints

### Environment
- Python 3.8 or higher required
- OpenAI API key must be set as environment variable: OPENAI_API_KEY

### Dependencies
- `openai` package for API integration
- Standard library only for other functionality (no additional external dependencies)

### Performance
- API calls should complete within reasonable time (< 30 seconds typical)
- CLI should be responsive to user input

### Output Format
- Terminal output: Colored text with emoji icons
- File output: Clean markdown format
- Filename pattern: meeting_notes_YYYY-MM-DD_HHMMSS.md

## Commands Reference

| Command | Description |
|---------|-------------|
| (paste transcript) | Input meeting transcript and get analysis |
| `save` | Save last analysis output to markdown file |
| `history` | Show summaries from current session |
| `q` | Quit the application |

## Non-Functional Requirements

### Usability
- Clear, intuitive command interface
- Helpful error messages
- Visual feedback during processing

### Reliability
- Graceful error handling for API failures
- Input validation
- File system error handling

### Maintainability
- Clean, modular code structure
- Clear separation of concerns
- Well-documented functions
