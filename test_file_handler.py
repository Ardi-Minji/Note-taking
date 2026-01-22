"""
Unit tests for file_handler module
"""

import pytest
import os
from datetime import datetime
from file_handler import (
    generate_filename, 
    save_to_file, 
    add_to_history, 
    get_history,
    format_history_display,
    _session_history
)


class TestGenerateFilename:
    """Tests for generate_filename function"""
    
    def test_generate_filename_format(self):
        """Test that filename follows the correct pattern"""
        filename = generate_filename()
        
        assert filename.startswith('meeting_notes_')
        assert filename.endswith('.md')
        assert len(filename) > 20  # Should include timestamp
        
    def test_generate_filename_unique(self):
        """Test that consecutive calls generate different filenames"""
        import time
        filename1 = generate_filename()
        time.sleep(1)  # Wait to ensure different timestamp
        filename2 = generate_filename()
        
        assert filename1 != filename2


class TestSaveToFile:
    """Tests for save_to_file function"""
    
    def test_save_to_file_creates_file(self):
        """Test that file is created"""
        analysis = {
            'summary': 'Test summary',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        filename = 'test_output.md'
        try:
            result = save_to_file(analysis, filename)
            assert os.path.exists(filename)
            assert result == filename
        finally:
            if os.path.exists(filename):
                os.remove(filename)
                
    def test_save_to_file_content(self):
        """Test that file contains analysis data"""
        analysis = {
            'summary': 'Unique test summary 12345',
            'action_items': ['Test action'],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        filename = 'test_content.md'
        try:
            save_to_file(analysis, filename)
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert 'Unique test summary 12345' in content
            assert 'Test action' in content
        finally:
            if os.path.exists(filename):
                os.remove(filename)


class TestSessionHistory:
    """Tests for session history functions"""
    
    def setup_method(self):
        """Clear history before each test"""
        _session_history.clear()
        
    def test_add_to_history(self):
        """Test adding analysis to history"""
        analysis = {
            'summary': 'Test',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        add_to_history(analysis)
        history = get_history()
        
        assert len(history) == 1
        assert history[0]['summary'] == 'Test'
        
    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy"""
        analysis = {
            'summary': 'Test',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        add_to_history(analysis)
        history1 = get_history()
        history2 = get_history()
        
        assert history1 is not history2
        
    def test_format_history_display_empty(self):
        """Test formatting empty history"""
        output = format_history_display()
        
        assert 'No meeting' in output or 'no meeting' in output.lower()
        
    def test_format_history_display_with_items(self):
        """Test formatting history with items"""
        analysis = {
            'summary': 'Test meeting summary',
            'action_items': [],
            'decisions': [],
            'questions': [],
            'attendees': [],
            'timestamp': datetime.now()
        }
        
        add_to_history(analysis)
        output = format_history_display()
        
        assert 'Test meeting summary' in output or 'Test meeting' in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
