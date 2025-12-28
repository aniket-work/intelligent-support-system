"""
Helper utilities for the Intelligent Support System
"""

import re
import logging
from datetime import datetime
from typing import Dict, Any, List
from .constants import ESCALATION_KEYWORDS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_ticket(ticket_text: str) -> Dict[str, Any]:
    """
    Parse raw ticket text into structured format
    
    Args:
        ticket_text: Raw ticket content
        
    Returns:
        Structured ticket dictionary
    """
    return {
        "id": generate_ticket_id(),
        "content": ticket_text,
        "timestamp": datetime.now().isoformat(),
        "metadata": extract_metadata(ticket_text)
    }


def generate_ticket_id() -> str:
    """Generate unique ticket ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"TKT-{timestamp}"


def extract_metadata(text: str) -> Dict[str, Any]:
    """
    Extract metadata from ticket text
    
    Args:
        text: Ticket content
        
    Returns:
        Metadata dictionary
    """
    metadata = {
        "word_count": len(text.split()),
        "has_email": bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
        "has_phone": bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)),
        "has_url": bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
        "escalation_keywords_found": find_escalation_keywords(text)
    }
    return metadata


def find_escalation_keywords(text: str) -> List[str]:
    """
    Find escalation keywords in text
    
    Args:
        text: Text to search
        
    Returns:
        List of found keywords
    """
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in ESCALATION_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords


def calculate_sentiment_score(text: str) -> float:
    """
    Simple sentiment scoring based on keywords
    
    Args:
        text: Text to analyze
        
    Returns:
        Sentiment score between -1 (negative) and 1 (positive)
    """
    positive_words = ["thank", "great", "excellent", "happy", "satisfied", "love", "appreciate"]
    negative_words = ["bad", "terrible", "awful", "hate", "angry", "frustrated", "disappointed", "poor"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    total = positive_count + negative_count
    if total == 0:
        return 0.0
    
    return (positive_count - negative_count) / total


def format_agent_response(agent_type: str, response: Dict[str, Any]) -> str:
    """
    Format agent response for logging
    
    Args:
        agent_type: Type of agent
        response: Agent response data
        
    Returns:
        Formatted string
    """
    return f"[{agent_type.upper()}] {response}"


def validate_ticket_data(ticket: Dict[str, Any]) -> bool:
    """
    Validate ticket data structure
    
    Args:
        ticket: Ticket dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["id", "content", "timestamp"]
    return all(field in ticket for field in required_fields)


def log_agent_action(agent_type: str, action: str, details: Dict[str, Any]):
    """
    Log agent actions for debugging
    
    Args:
        agent_type: Type of agent
        action: Action performed
        details: Additional details
    """
    logger.info(f"[{agent_type}] {action}: {details}")
