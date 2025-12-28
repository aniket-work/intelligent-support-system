"""
Router Agent - Routes classified tickets to appropriate departments
"""

import yaml
from typing import Dict, Any
from utils.constants import Department, Priority
from utils.helpers import log_agent_action


class RouterAgent:
    """
    Agent responsible for routing tickets to appropriate departments
    """
    
    def __init__(self, config_path: str = "config/settings.yaml", prompts_path: str = "config/prompts.yaml"):
        """
        Initialize the router agent
        
        Args:
            config_path: Path to settings configuration
            prompts_path: Path to prompts configuration
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        with open(prompts_path, 'r') as f:
            self.prompts = yaml.safe_load(f)
        
        self.agent_config = self.config['agents']['router']
        self.department_mappings = self.config['department_mappings']
    
    def route_ticket(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a classified ticket to appropriate department
        
        Args:
            classification: Classification results from classifier agent
            
        Returns:
            Routing decision
        """
        log_agent_action("ROUTER", "Starting routing", {"ticket_id": classification['ticket_id']})
        
        category = classification['category']
        priority = classification['priority']
        
        # Determine primary department
        primary_department = self._select_department(category, priority)
        
        # Determine if escalation is needed
        needs_escalation = self._check_escalation_needed(priority, classification)
        
        routing = {
            "ticket_id": classification['ticket_id'],
            "primary_department": primary_department,
            "backup_departments": self._get_backup_departments(category),
            "needs_escalation": needs_escalation,
            "routing_confidence": 0.90  # Simulated confidence
        }
        
        log_agent_action("ROUTER", "Routing complete", routing)
        
        return routing
    
    def _select_department(self, category: str, priority: str) -> str:
        """
        Select primary department based on category and priority
        
        Args:
            category: Ticket category
            priority: Ticket priority
            
        Returns:
            Department name
        """
        # Get possible departments for category
        possible_departments = self.department_mappings.get(category, [Department.CUSTOMER_SUCCESS])
        
        # If urgent or high priority, prefer escalation team if available
        if priority in [Priority.URGENT, Priority.HIGH] and Department.ESCALATION_TEAM in possible_departments:
            return Department.ESCALATION_TEAM
        
        # Otherwise return first department
        return possible_departments[0]
    
    def _get_backup_departments(self, category: str) -> list:
        """
        Get backup departments for a category
        
        Args:
            category: Ticket category
            
        Returns:
            List of backup departments
        """
        all_departments = self.department_mappings.get(category, [])
        return all_departments[1:] if len(all_departments) > 1 else []
    
    def _check_escalation_needed(self, priority: str, classification: Dict[str, Any]) -> bool:
        """
        Check if ticket needs escalation
        
        Args:
            priority: Ticket priority
            classification: Classification data
            
        Returns:
            True if escalation needed
        """
        # Escalate urgent tickets
        if priority == Priority.URGENT:
            return True
        
        # Escalate high priority with negative sentiment
        if priority == Priority.HIGH and classification.get('sentiment_score', 0) < -0.5:
            return True
        
        return False
