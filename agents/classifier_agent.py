"""
Classifier Agent - Analyzes and classifies customer support tickets
"""

import yaml
from typing import Dict, Any
from utils.constants import TicketCategory, Priority, TicketStatus
from utils.helpers import calculate_sentiment_score, find_escalation_keywords, log_agent_action


class ClassifierAgent:
    """
    Agent responsible for classifying incoming support tickets
    """
    
    def __init__(self, config_path: str = "config/settings.yaml", prompts_path: str = "config/prompts.yaml"):
        """
        Initialize the classifier agent
        
        Args:
            config_path: Path to settings configuration
            prompts_path: Path to prompts configuration
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        with open(prompts_path, 'r') as f:
            self.prompts = yaml.safe_load(f)
        
        self.agent_config = self.config['agents']['classifier']
        self.priority_thresholds = self.config['priority_thresholds']
    
    def classify_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a support ticket
        
        Args:
            ticket: Ticket dictionary with content and metadata
            
        Returns:
            Classification results
        """
        log_agent_action("CLASSIFIER", "Starting classification", {"ticket_id": ticket['id']})
        
        # Extract content
        content = ticket['content']
        
        # Analyze content
        category = self._determine_category(content)
        priority = self._determine_priority(content, ticket.get('metadata', {}))
        sentiment_score = calculate_sentiment_score(content)
        key_issues = self._extract_key_issues(content)
        
        classification = {
            "ticket_id": ticket['id'],
            "category": category,
            "priority": priority,
            "sentiment_score": sentiment_score,
            "key_issues": key_issues,
            "status": TicketStatus.CLASSIFIED,
            "classifier_confidence": 0.85  # Simulated confidence score
        }
        
        log_agent_action("CLASSIFIER", "Classification complete", classification)
        
        return classification
    
    def _determine_category(self, content: str) -> str:
        """
        Determine ticket category based on content
        
        Args:
            content: Ticket content
            
        Returns:
            Category string
        """
        content_lower = content.lower()
        
        # Technical keywords
        technical_keywords = ["error", "bug", "crash", "not working", "broken", "issue", "problem", "technical"]
        if any(keyword in content_lower for keyword in technical_keywords):
            return TicketCategory.TECHNICAL
        
        # Billing keywords
        billing_keywords = ["payment", "charge", "billing", "invoice", "refund", "subscription", "price"]
        if any(keyword in content_lower for keyword in billing_keywords):
            return TicketCategory.BILLING
        
        # Account keywords
        account_keywords = ["account", "login", "password", "access", "username", "profile"]
        if any(keyword in content_lower for keyword in account_keywords):
            return TicketCategory.ACCOUNT
        
        # Feature request keywords
        feature_keywords = ["feature", "request", "suggestion", "enhancement", "would like", "could you add"]
        if any(keyword in content_lower for keyword in feature_keywords):
            return TicketCategory.FEATURE_REQUEST
        
        return TicketCategory.GENERAL
    
    def _determine_priority(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Determine ticket priority
        
        Args:
            content: Ticket content
            metadata: Ticket metadata
            
        Returns:
            Priority level
        """
        sentiment_score = calculate_sentiment_score(content)
        escalation_keywords = metadata.get('escalation_keywords_found', [])
        
        # Check for urgent priority
        if (sentiment_score <= self.priority_thresholds['urgent']['sentiment_score'] or
            len(escalation_keywords) >= self.priority_thresholds['urgent']['escalation_keyword_count']):
            return Priority.URGENT
        
        # Check for high priority
        if (sentiment_score <= self.priority_thresholds['high']['sentiment_score'] or
            len(escalation_keywords) >= self.priority_thresholds['high']['escalation_keyword_count']):
            return Priority.HIGH
        
        # Check for medium priority
        if sentiment_score <= self.priority_thresholds['medium']['sentiment_score']:
            return Priority.MEDIUM
        
        return Priority.LOW
    
    def _extract_key_issues(self, content: str) -> list:
        """
        Extract key issues from ticket content
        
        Args:
            content: Ticket content
            
        Returns:
            List of key issues
        """
        # Simple extraction based on sentences
        sentences = content.split('.')
        key_issues = [s.strip() for s in sentences if len(s.strip()) > 20][:3]
        
        return key_issues
