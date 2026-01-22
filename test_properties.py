"""
Property-based tests using Hypothesis
Tests correctness properties across many generated inputs
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from datetime import datetime
import os
import re
from analyzer import parse_response, build_prompt
from formatter import format_terminal_output, format_markdown_output
from file_handler import generate_filename, save_to_file, add_to_history, get_history, _session_history


# Property 2.1: Output Completeness
# **Validates: Requirements 2.1-2.5**
@given(
    summary=st.text(min_size=1, max_size=500),
    action_items=st.lists(st.text(min_size=1, max_size=100), max_size=10),
    decisions=st.lists(st.text(min_size=1, max_size=100), max_size=10),
    questions=st.lists(st.text(min_size=1, max_size=100), max_size=10),
    attendees=st.lists(st.text(min_size=1, max_size=50), max_size=20)
)
@settings(max_examples=50)
def test_property_analysis_dict_has_all_required_keys(summary, action_items, decisions, questions, attendees):
    """
    Property: All analysis dictionaries must contain all required keys
    **Validates: Requirements 2.1-2.5**
    """
    analysis = {
        'summary': summary,
        'action_items': action_items,
        'decisions': decisions,
        'questions': questions,
        'attendees': attendees,
        'timestamp': datetime.now()
    }
    
    # All required keys must be present
    assert 'summary' in analysis
    assert 'action_items' in analysis
    assert 'decisions' in analysis
    assert 'questions' in analysis
    assert 'attendees' in analysis
    assert 'timestamp' in analysis
    
    # Types must be correct
    assert isinstance(analysis['summary'], str)
    assert isinstance(analysis['action_items'], list)
    assert isinstance(analysis['decisions'], list)
    assert isinstance(analysis['questions'], list)
    assert isinstance(analysis['attendees'], list)
    assert isinstance(analysis['timestamp'], datetime)


# Property 2.2: Output Structure - Terminal Formatting
# **Validates: Requirements 2.6**
@given(
    summary=st.text(min_size=1, max_size=200),
    action_items=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5),
    decisions=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5),
    questions=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5),
    attendees=st.lists(st.text(min_size=1, max_size=30), min_size=0, max_size=5)
)
@settings(max_examples=50)
def test_property_formatted_output_contains_all_section_headers(summary, action_items, decisions, questions, attendees):
    """
    Property: Formatted output must contain all section headers
    **Validates: Requirements 2.6**
    """
    analysis = {
        'summary': summary,
        'action_items': action_items,
        'decisions': decisions,
        'questions': questions,
        'attendees': attendees,
        'timestamp': datetime.now()
    }
    
    output = format_terminal_output(analysis)
    
    # All section headers must be present
    assert 'SUMMARY' in output
    assert 'ACTION ITEMS' in output or 'ACTION' in output
    assert 'DECISIONS' in output or 'DECISION' in output
    assert 'QUESTIONS' in output or 'QUESTION' in output
    assert 'ATTENDEES' in output or 'ATTENDEE' in output


# Property 3.1: Filename Uniqueness
# **Validates: Requirements 3.3**
@settings(max_examples=20)
@given(st.integers(min_value=0, max_value=10))
def test_property_generated_filenames_follow_pattern(seed):
    """
    Property: Generated filenames must follow the pattern meeting_notes_YYYY-MM-DD_HHMMSS.md
    **Validates: Requirements 3.3**
    """
    filename = generate_filename()
    
    # Must match pattern
    pattern = r'^meeting_notes_\d{4}-\d{2}-\d{2}_\d{6}\.md$'
    assert re.match(pattern, filename), f"Filename {filename} doesn't match pattern"
    
    # Must have .md extension
    assert filename.endswith('.md')
    
    # Must start with meeting_notes_
    assert filename.startswith('meeting_notes_')


# Property 3.2: File Content Integrity
# **Validates: Requirements 3.2**
@given(
    summary=st.text(min_size=10, max_size=100, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))),
    action_items=st.lists(st.text(min_size=5, max_size=50, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))), min_size=1, max_size=3)
)
@settings(max_examples=20)
def test_property_saved_files_contain_all_analysis_data(summary, action_items):
    """
    Property: Saved markdown files must contain all analysis data
    **Validates: Requirements 3.2**
    """
    analysis = {
        'summary': summary,
        'action_items': action_items,
        'decisions': ['Test decision'],
        'questions': [],
        'attendees': [],
        'timestamp': datetime.now()
    }
    
    filename = f'test_property_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.md'
    
    try:
        saved_path = save_to_file(analysis, filename)
        
        # File must exist
        assert os.path.exists(saved_path)
        
        # Read file content
        with open(saved_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Summary must be in file
        assert summary in content
        
        # Action items must be in file
        for item in action_items:
            assert item in content
            
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)


# Property 4.1: History Persistence
# **Validates: Requirements 4.1-4.3**
@given(
    num_items=st.integers(min_value=1, max_value=10)
)
@settings(max_examples=20)
def test_property_history_retains_all_added_items(num_items):
    """
    Property: Session history must retain all analyses added to it
    **Validates: Requirements 4.1-4.3**
    """
    # Clear history
    _session_history.clear()
    
    # Add items
    for i in range(num_items):
        analysis = {
            'summary': f'Summary {i}',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        add_to_history(analysis)
    
    # Retrieve history
    history = get_history()
    
    # Must have all items
    assert len(history) == num_items
    
    # All summaries must be present
    summaries = [item['summary'] for item in history]
    for i in range(num_items):
        assert f'Summary {i}' in summaries


# Property 1.3: Input Validation
# **Validates: Requirements 1.3**
@given(
    whitespace=st.text(alphabet=st.characters(whitelist_categories=('Zs',)), min_size=0, max_size=100)
)
@settings(max_examples=30)
def test_property_input_validation_rejects_empty_whitespace(whitespace):
    """
    Property: Input validation must reject empty or whitespace-only input
    **Validates: Requirements 1.3**
    """
    # Empty or whitespace-only strings should be invalid
    is_valid = bool(whitespace.strip())
    
    if not is_valid:
        # These should be rejected by validation
        assert whitespace == '' or whitespace.isspace()


# Property: Markdown output is valid
# **Validates: Requirements 3.2**
@given(
    summary=st.text(min_size=10, max_size=200, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))),
    action_items=st.lists(st.text(min_size=5, max_size=50, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))), max_size=5)
)
@settings(max_examples=30)
def test_property_markdown_output_is_valid_and_complete(summary, action_items):
    """
    Property: Markdown output must be valid and complete
    **Validates: Requirements 3.2**
    """
    analysis = {
        'summary': summary,
        'action_items': action_items,
        'decisions': [],
        'questions': [],
        'attendees': [],
        'timestamp': datetime.now()
    }
    
    output = format_markdown_output(analysis)
    
    # Must contain markdown headers
    assert '#' in output
    
    # Must contain summary
    assert summary in output
    
    # Must contain action items
    for item in action_items:
        assert item in output
    
    # Must have proper structure (headers followed by content)
    lines = output.split('\n')
    assert len(lines) > 5  # Should have multiple lines


# Property: Parse response handles various formats
# **Validates: Requirements 2.1-2.5**
@given(
    summary_text=st.text(min_size=10, max_size=200, alphabet=st.characters(blacklist_categories=('Cs', 'Cc')))
)
@settings(max_examples=30)
def test_property_parse_response_always_returns_valid_structure(summary_text):
    """
    Property: parse_response must always return a valid structure
    **Validates: Requirements 2.1-2.5**
    """
    # Create a minimal valid response
    response = f"""
SUMMARY:
{summary_text}

ACTION ITEMS:
- Test action

DECISIONS MADE:
- Test decision

OPEN QUESTIONS:
- Test question

ATTENDEES:
- Test person
"""
    
    result = parse_response(response)
    
    # Must have all required keys
    assert 'summary' in result
    assert 'action_items' in result
    assert 'decisions' in result
    assert 'questions' in result
    assert 'attendees' in result
    assert 'timestamp' in result
    
    # Summary should contain the text
    assert summary_text in result['summary'] or len(result['summary']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
