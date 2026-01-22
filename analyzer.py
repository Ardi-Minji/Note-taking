"""
Meeting Notes AI - AI Analysis Module
Handles OpenAI API integration and transcript analysis.
"""

import os
import re
import time
from datetime import datetime
from typing import Dict, List
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

# Constants
MODEL = "gpt-4o-mini"
MAX_TOKENS = 1500
TEMPERATURE = 0.7

# Initialize OpenAI client
_client = None

def get_client():
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client


def build_prompt(transcript: str) -> str:
    """
    Construct the AI prompt for meeting transcript analysis.
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Formatted prompt string for the AI
    """
    prompt = f"""Analyze the following meeting transcript and extract key information.

Please provide your analysis in the following structured format:

SUMMARY:
[Provide a concise 3-5 sentence summary of the meeting]

ACTION ITEMS:
[List each action item on a new line, prefixed with "- ". Include assigned person if mentioned]

DECISIONS MADE:
[List each decision on a new line, prefixed with "- "]

OPEN QUESTIONS:
[List each open question or follow-up on a new line, prefixed with "- "]

ATTENDEES:
[List each attendee on a new line, prefixed with "- ". Only include if explicitly mentioned]

Meeting Transcript:
{transcript}
"""
    return prompt


def parse_response(response: str) -> Dict[str, any]:
    """
    Parse AI response into structured data.
    
    Args:
        response: Raw response text from AI
        
    Returns:
        Dictionary containing parsed sections
    """
    result = {
        'summary': '',
        'action_items': [],
        'decisions': [],
        'questions': [],
        'attendees': [],
        'timestamp': datetime.now()
    }
    
    # Split response into sections
    sections = {
        'SUMMARY:': 'summary',
        'ACTION ITEMS:': 'action_items',
        'DECISIONS MADE:': 'decisions',
        'OPEN QUESTIONS:': 'questions',
        'ATTENDEES:': 'attendees'
    }
    
    current_section = None
    lines = response.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line is a section header
        section_found = False
        for header, key in sections.items():
            if header in line.upper():
                current_section = key
                section_found = True
                break
        
        if section_found:
            continue
            
        # Add content to current section
        if current_section:
            if current_section == 'summary':
                if result['summary']:
                    result['summary'] += ' ' + line
                else:
                    result['summary'] = line
            else:
                # Remove bullet points and dashes
                cleaned_line = re.sub(r'^[-•*]\s*', '', line)
                if cleaned_line and cleaned_line.lower() not in ['none', 'n/a', 'not mentioned', 'not mentioned in transcript']:
                    result[current_section].append(cleaned_line)
    
    return result


def analyze_transcript_demo(transcript: str) -> Dict[str, any]:
    """
    Demo mode: Analyze transcript using pattern matching (no API call).
    Provides a working demo without requiring an API key.
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing structured analysis results
    """
    lines = transcript.split('\n')
    
    # Extract potential attendees (names followed by colon)
    attendees = []
    for line in lines:
        if ':' in line:
            name = line.split(':')[0].strip()
            if name and len(name.split()) <= 3 and name[0].isupper():
                if name not in attendees:
                    attendees.append(name)
    
    # Generate demo summary
    summary = f"Demo analysis of meeting transcript with {len(attendees)} participants. " \
              f"The transcript contains {len(lines)} lines of discussion. " \
              f"This is a demonstration mode - connect an OpenAI API key for AI-powered analysis."
    
    # Extract action items (lines with "will", "should", "need to", etc.)
    action_keywords = ['will', 'should', 'need to', 'must', 'have to', 'going to', 'can you']
    action_items = []
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in action_keywords):
            # Clean up the line
            if ':' in line:
                line = line.split(':', 1)[1].strip()
            if line and len(line) > 10:
                action_items.append(line[:100])
    
    # Extract decisions (lines with "decided", "agreed", "approved", etc.)
    decision_keywords = ['decided', 'agreed', 'approved', 'confirmed', 'let\'s', 'we will']
    decisions = []
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in decision_keywords):
            if ':' in line:
                line = line.split(':', 1)[1].strip()
            if line and len(line) > 10:
                decisions.append(line[:100])
    
    # Extract questions (lines with "?")
    questions = []
    for line in lines:
        if '?' in line:
            if ':' in line:
                line = line.split(':', 1)[1].strip()
            if line:
                questions.append(line[:100])
    
    return {
        'summary': summary,
        'action_items': action_items[:10],  # Limit to 10
        'decisions': decisions[:10],
        'questions': questions[:10],
        'attendees': attendees[:20],
        'timestamp': datetime.now()
    }


def analyze_transcript(transcript: str, retry_count: int = 2, use_demo: bool = False) -> Dict[str, any]:
    """
    Analyze meeting transcript using OpenAI API or demo mode.
    
    Args:
        transcript: The meeting transcript text
        retry_count: Number of retries for transient failures
        use_demo: If True, use demo mode without API calls
        
    Returns:
        Dictionary containing structured analysis results
        
    Raises:
        Exception: If API call fails after retries (when not in demo mode)
    """
    # Use demo mode if requested or if API key is not available
    if use_demo:
        return analyze_transcript_demo(transcript)
    
    # Try to use API, fall back to demo if it fails
    last_error = None
    
    for attempt in range(retry_count + 1):
        try:
            client = get_client()
            prompt = build_prompt(transcript)
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes meeting transcripts and extracts key information."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            # Parse and return structured data
            return parse_response(response_text)
            
        except RateLimitError as e:
            last_error = e
            if attempt < retry_count:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"\n\033[93mRate limit reached. Waiting {wait_time} seconds before retry...\033[0m")
                time.sleep(wait_time)
            else:
                raise Exception("Rate limit exceeded. Please try again later.")
                
        except APIConnectionError as e:
            last_error = e
            if attempt < retry_count:
                wait_time = (attempt + 1) * 2
                print(f"\n\033[93mConnection error. Retrying in {wait_time} seconds...\033[0m")
                time.sleep(wait_time)
            else:
                raise Exception("Failed to connect to OpenAI API. Please check your internet connection.")
                
        except APIError as e:
            last_error = e
            raise Exception(f"OpenAI API error: {str(e)}")
            
        except Exception as e:
            last_error = e
            raise Exception(f"Failed to analyze transcript: {str(e)}")
    
    # If we get here, all retries failed
    raise Exception(f"Failed to analyze transcript after {retry_count} retries: {str(last_error)}")
