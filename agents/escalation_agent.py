"""
Escalation Agent - Handles ticket escalation decisions
"""

import yaml
from typing import Dict, Any
from utils.constants import Priority
from utils.helpers import log_agent_action


class EscalationAgent:
    """
    Agent responsible for escalation decisions
    """
    
    def __init__(self, config_path: str = "config/settings.yaml", prompts_path: str = "config/prompts.yaml"):
        """
        Initialize the escalation agent
        
        Args:
            config_path: Path to settings configuration
            prompts_path: Path to prompts configuration
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        with open(prompts_path, 'r') as f:
            self.prompts = yaml.safe_load(f)
        
        self.agent_config = self.config['agents']['escalation_handler']
    
    def evaluate_escalation(self, ticket: Dict[str, Any], classification: Dict[str, Any], 
                           routing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate if ticket needs escalation
        
        Args:
            ticket: Original ticket data
            classification: Classification results
            routing: Routing decision
            
        Returns:
            Escalation decision
        """
        log_agent_action("ESCALATION", "Evaluating escalation", {"ticket_id": ticket['id']})
        
        priority = classification['priority']
        sentiment_score = classification.get('sentiment_score', 0)
        escalation_keywords = ticket.get('metadata', {}).get('escalation_keywords_found', [])
        
        # Determine if escalation is needed
        needs_escalation, escalation_reason = self._check_escalation_criteria(
            priority, sentiment_score, escalation_keywords
        )
        
        # Determine escalation level
        escalation_level = self._determine_escalation_level(priority, sentiment_score)
        
        escalation = {
            "ticket_id": ticket['id'],
            "needs_escalation": needs_escalation,
            "escalation_level": escalation_level,
            "escalation_reason": escalation_reason,
            "recommended_action": self._get_recommended_action(needs_escalation, escalation_level),
            "human_review_required": needs_escalation
        }
        
        log_agent_action("ESCALATION", "Escalation evaluation complete", escalation)
        
        return escalation
    
    def _check_escalation_criteria(self, priority: str, sentiment_score: float, 
                                   escalation_keywords: list) -> tuple:
        """
        Check if ticket meets escalation criteria
        
        Args:
            priority: Ticket priority
            sentiment_score: Sentiment score
            escalation_keywords: List of escalation keywords found
            
        Returns:
            Tuple of (needs_escalation, reason)
        """
        # Urgent priority always escalates
        if priority == Priority.URGENT:
            return True, "Urgent priority ticket"
        
        # High priority with negative sentiment
        if priority == Priority.HIGH and sentiment_score < -0.5:
            return True, "High priority with negative sentiment"
        
        # Multiple escalation keywords
        if len(escalation_keywords) >= 2:
            return True, f"Multiple escalation keywords found: {', '.join(escalation_keywords)}"
        
        # Legal/compliance keywords
        legal_keywords = ["legal", "lawsuit", "attorney", "lawyer"]
        if any(keyword in escalation_keywords for keyword in legal_keywords):
            return True, "Legal/compliance issue detected"
        
        return False, "No escalation criteria met"
    
    def _determine_escalation_level(self, priority: str, sentiment_score: float) -> int:
        """
        Determine escalation level (1-3)
        
        Args:
            priority: Ticket priority
            sentiment_score: Sentiment score
            
        Returns:
            Escalation level
        """
        if priority == Priority.URGENT and sentiment_score < -0.7:
            return 3  # Critical escalation
        elif priority == Priority.URGENT or (priority == Priority.HIGH and sentiment_score < -0.5):
            return 2  # High escalation
        else:
            return 1  # Standard escalation
    
    def _get_recommended_action(self, needs_escalation: bool, escalation_level: int) -> str:
        """
        Get recommended action based on escalation decision
        
        Args:
            needs_escalation: Whether escalation is needed
            escalation_level: Level of escalation
            
        Returns:
            Recommended action string
        """
        if not needs_escalation:
            return "Process through standard workflow"
        
        if escalation_level == 3:
            return "Immediate human intervention required - Notify senior support manager"
        elif escalation_level == 2:
            return "Route to escalation team - Response required within 2 hours"
        else:
            return "Flag for supervisor review - Response required within 24 hours"
