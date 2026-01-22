"""
Meeting Notes AI - Output Formatting Module
Handles formatting of analysis results for terminal and file output.
"""

from typing import Dict
from datetime import datetime


def format_terminal_output(analysis: Dict[str, any]) -> str:
    """
    Format analysis results for colored terminal display.
    
    Args:
        analysis: Dictionary containing analysis results
        
    Returns:
        Formatted string with ANSI color codes and emojis
    """
    output = []
    
    # Summary section
    output.append("\n\033[96m\033[1m📝 SUMMARY\033[0m")
    output.append(analysis.get('summary', 'No summary available'))
    
    # Action Items section
    output.append("\n\033[96m\033[1m✅ ACTION ITEMS\033[0m")
    action_items = analysis.get('action_items', [])
    if action_items:
        for item in action_items:
            output.append(f"  • {item}")
    else:
        output.append("  No action items identified")
    
    # Decisions section
    output.append("\n\033[96m\033[1m📅 DECISIONS MADE\033[0m")
    decisions = analysis.get('decisions', [])
    if decisions:
        for decision in decisions:
            output.append(f"  • {decision}")
    else:
        output.append("  No decisions identified")
    
    # Open Questions section
    output.append("\n\033[96m\033[1m❓ OPEN QUESTIONS / FOLLOW-UPS\033[0m")
    questions = analysis.get('questions', [])
    if questions:
        for question in questions:
            output.append(f"  • {question}")
    else:
        output.append("  No open questions identified")
    
    # Attendees section
    output.append("\n\033[96m\033[1m👥 ATTENDEES\033[0m")
    attendees = analysis.get('attendees', [])
    if attendees:
        for attendee in attendees:
            output.append(f"  • {attendee}")
    else:
        output.append("  Not mentioned in transcript")
    
    return "\n".join(output)


def format_markdown_output(analysis: Dict[str, any]) -> str:
    """
    Format analysis results as clean markdown.
    
    Args:
        analysis: Dictionary containing analysis results
        
    Returns:
        Formatted markdown string
    """
    output = []
    
    # Header with timestamp
    timestamp = analysis.get('timestamp', datetime.now())
    output.append(f"# Meeting Notes - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    
    # Summary section
    output.append("## 📝 Summary")
    output.append(analysis.get('summary', 'No summary available'))
    output.append("")
    
    # Action Items section
    output.append("## ✅ Action Items")
    action_items = analysis.get('action_items', [])
    if action_items:
        for item in action_items:
            output.append(f"- {item}")
    else:
        output.append("- No action items identified")
    output.append("")
    
    # Decisions section
    output.append("## 📅 Decisions Made")
    decisions = analysis.get('decisions', [])
    if decisions:
        for decision in decisions:
            output.append(f"- {decision}")
    else:
        output.append("- No decisions identified")
    output.append("")
    
    # Open Questions section
    output.append("## ❓ Open Questions / Follow-ups")
    questions = analysis.get('questions', [])
    if questions:
        for question in questions:
            output.append(f"- {question}")
    else:
        output.append("- No open questions identified")
    output.append("")
    
    # Attendees section
    output.append("## 👥 Attendees")
    attendees = analysis.get('attendees', [])
    if attendees:
        for attendee in attendees:
            output.append(f"- {attendee}")
    else:
        output.append("- Not mentioned in transcript")
    
    return "\n".join(output)
