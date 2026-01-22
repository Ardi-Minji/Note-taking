"""
Unit tests for analyzer module
"""

import pytest
from unittest.mock import Mock, patch
from analyzer import build_prompt, parse_response, analyze_transcript
from datetime import datetime


class TestBuildPrompt:
    """Tests for build_prompt function"""
    
    def test_build_prompt_includes_transcript(self):
        """Test that prompt includes the transcript text"""
        transcript = "Test meeting content"
        prompt = build_prompt(transcript)
        assert transcript in prompt
        
    def test_build_prompt_includes_sections(self):
        """Test that prompt requests all required sections"""
        prompt = build_prompt("test")
        assert "SUMMARY" in prompt.upper()
        assert "ACTION ITEMS" in prompt.upper()
        assert "DECISIONS" in prompt.upper()
        assert "OPEN QUESTIONS" in prompt.upper() or "FOLLOW" in prompt.upper()
        assert "ATTENDEES" in prompt.upper()


class TestParseResponse:
    """Tests for parse_response function"""
    
    def test_parse_response_basic_structure(self):
        """Test parsing a well-formatted response"""
        response = """
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
        result = parse_response(response)
        
        assert 'summary' in result
        assert 'action_items' in result
        assert 'decisions' in result
        assert 'questions' in result
        assert 'attendees' in result
        assert 'timestamp' in result
        
    def test_parse_response_extracts_summary(self):
        """Test that summary is extracted correctly"""
        response = """
SUMMARY:
This is a test summary.

ACTION ITEMS:
- None
"""
        result = parse_response(response)
        assert "test summary" in result['summary'].lower()
        
    def test_parse_response_extracts_action_items(self):
        """Test that action items are extracted as list"""
        response = """
SUMMARY:
Test

ACTION ITEMS:
- Task 1
- Task 2
"""
        result = parse_response(response)
        assert len(result['action_items']) == 2
        assert "Task 1" in result['action_items']
        
    def test_parse_response_handles_missing_sections(self):
        """Test that missing sections don't break parsing"""
        response = """
SUMMARY:
Just a summary
"""
        result = parse_response(response)
        assert result['summary']
        assert isinstance(result['action_items'], list)
        assert isinstance(result['decisions'], list)


class TestAnalyzeTranscript:
    """Tests for analyze_transcript function"""
    
    @patch('analyzer.get_client')
    def test_analyze_transcript_calls_api(self, mock_get_client):
        """Test that analyze_transcript calls OpenAI API"""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
SUMMARY:
Test summary

ACTION ITEMS:
- Test action

DECISIONS MADE:
- Test decision

OPEN QUESTIONS:
- Test question

ATTENDEES:
- Test person
"""
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = analyze_transcript("Test transcript")
        
        assert mock_client.chat.completions.create.called
        assert 'summary' in result
        assert 'action_items' in result
        
    @patch('analyzer.get_client')
    def test_analyze_transcript_handles_api_error(self, mock_get_client):
        """Test that API errors are handled gracefully"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client
        
        with pytest.raises(Exception) as exc_info:
            analyze_transcript("Test transcript")
        
        assert "Failed to analyze transcript" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
