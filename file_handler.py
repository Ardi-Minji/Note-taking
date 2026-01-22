"""
Meeting Notes AI - File Operations Module
Handles file saving and session history management.
"""

import os
from datetime import datetime
from typing import Dict, List


# Session history storage (in-memory)
_session_history: List[Dict] = []


def generate_filename() -> str:
    """
    Generate timestamped filename for meeting notes.
    
    Returns:
        Filename in format: meeting_notes_YYYY-MM-DD_HHMMSS.md
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"meeting_notes_{timestamp}.md"


def save_to_file(analysis: Dict[str, any], filename: str = None) -> str:
    """
    Save analysis results to a markdown file.
    
    Args:
        analysis: Dictionary containing analysis results
        filename: Optional custom filename (auto-generated if not provided)
        
    Returns:
        Path to the saved file
        
    Raises:
        IOError: If file cannot be written
    """
    from formatter import format_markdown_output
    
    try:
        # Generate filename if not provided
        if filename is None:
            filename = generate_filename()
        
        # Ensure filename has .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Get markdown content
        content = format_markdown_output(analysis)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
        
    except PermissionError:
        raise IOError(f"Permission denied: Cannot write to {filename}")
    except OSError as e:
        raise IOError(f"Failed to save file: {str(e)}")


def add_to_history(analysis: Dict[str, any]) -> None:
    """
    Add analysis to session history.
    
    Args:
        analysis: Dictionary containing analysis results
    """
    _session_history.append(analysis)


def get_history() -> List[Dict]:
    """
    Retrieve session history.
    
    Returns:
        List of analysis dictionaries from current session
    """
    return _session_history.copy()


def format_history_display() -> str:
    """
    Format session history for terminal display.
    
    Returns:
        Formatted string showing all meeting summaries from session
    """
    if not _session_history:
        return "\n\033[93mNo meeting analyses in current session.\033[0m"
    
    output = ["\n\033[96m\033[1m📚 SESSION HISTORY\033[0m\n"]
    
    for idx, analysis in enumerate(_session_history, 1):
        timestamp = analysis.get('timestamp', datetime.now())
        summary = analysis.get('summary', 'No summary available')
        
        output.append(f"\033[1m{idx}. Meeting at {timestamp.strftime('%H:%M:%S')}\033[0m")
        output.append(f"   {summary[:100]}{'...' if len(summary) > 100 else ''}")
        output.append("")
    
    return "\n".join(output)
