"""
Unit tests for formatter module
"""

import pytest
from formatter import format_terminal_output, format_markdown_output
from datetime import datetime


class TestFormatTerminalOutput:
    """Tests for format_terminal_output function"""
    
    def test_format_terminal_output_includes_all_sections(self):
        """Test that all sections are included in output"""
        analysis = {
            'summary': 'Test summary',
            'action_items': ['Action 1'],
            'decisions': ['Decision 1'],
            'questions': ['Question 1'],
            'attendees': ['Person 1'],
            'timestamp': datetime.now()
        }
        
        output = format_terminal_output(analysis)
        
        assert 'SUMMARY' in output
        assert 'ACTION ITEMS' in output
        assert 'DECISIONS' in output
        assert 'QUESTIONS' in output or 'FOLLOW' in output
        assert 'ATTENDEES' in output
        
    def test_format_terminal_output_includes_content(self):
        """Test that content is included in output"""
        analysis = {
            'summary': 'Test summary content',
            'action_items': ['Action item 1'],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        output = format_terminal_output(analysis)
        
        assert 'Test summary content' in output
        assert 'Action item 1' in output
        
    def test_format_terminal_output_handles_empty_sections(self):
        """Test that empty sections are handled gracefully"""
        analysis = {
            'summary': 'Test',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        output = format_terminal_output(analysis)
        
        # Should not crash and should indicate no items
        assert output
        assert 'No action items' in output or 'action items' in output.lower()


class TestFormatMarkdownOutput:
    """Tests for format_markdown_output function"""
    
    def test_format_markdown_output_valid_markdown(self):
        """Test that output is valid markdown"""
        analysis = {
            'summary': 'Test summary',
            'action_items': ['Action 1'],
            'decisions': ['Decision 1'],
            'questions': ['Question 1'],
            'attendees': ['Person 1'],
            'timestamp': datetime.now()
        }
        
        output = format_markdown_output(analysis)
        
        # Check for markdown headers
        assert '##' in output or '#' in output
        # Check for lists
        assert '-' in output
        
    def test_format_markdown_output_includes_timestamp(self):
        """Test that timestamp is included"""
        timestamp = datetime(2026, 1, 22, 10, 30, 0)
        analysis = {
            'summary': 'Test',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': timestamp
        }
        
        output = format_markdown_output(analysis)
        
        assert '2026' in output
        
    def test_format_markdown_output_includes_all_sections(self):
        """Test that all sections are present"""
        analysis = {
            'summary': 'Summary text',
            'action_items': ['Item 1'],
            'decisions': ['Decision 1'],
            'questions': ['Question 1'],
            'attendees': ['Person 1'],
            'timestamp': datetime.now()
        }
        
        output = format_markdown_output(analysis)
        
        assert 'Summary' in output
        assert 'Action Items' in output or 'ACTION ITEMS' in output
        assert 'Decisions' in output or 'DECISIONS' in output
        assert 'Questions' in output or 'QUESTIONS' in output
        assert 'Attendees' in output or 'ATTENDEES' in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
