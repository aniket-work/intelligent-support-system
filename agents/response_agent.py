"""
Response Agent - Generates professional responses to customer tickets
"""

import yaml
from typing import Dict, Any
from utils.constants import TicketCategory, Priority
from utils.helpers import log_agent_action


class ResponseAgent:
    """
    Agent responsible for generating customer responses
    """
    
    def __init__(self, config_path: str = "config/settings.yaml", prompts_path: str = "config/prompts.yaml"):
        """
        Initialize the response agent
        
        Args:
            config_path: Path to settings configuration
            prompts_path: Path to prompts configuration
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        with open(prompts_path, 'r') as f:
            self.prompts = yaml.safe_load(f)
        
        self.agent_config = self.config['agents']['response_generator']
    
    def generate_response(self, ticket: Dict[str, Any], classification: Dict[str, Any], 
                         routing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a professional response to the ticket
        
        Args:
            ticket: Original ticket data
            classification: Classification results
            routing: Routing decision
            
        Returns:
            Generated response
        """
        log_agent_action("RESPONSE", "Generating response", {"ticket_id": ticket['id']})
        
        category = classification['category']
        priority = classification['priority']
        department = routing['primary_department']
        
        # Generate response based on category
        response_text = self._create_response(ticket['content'], category, priority, department)
        
        response = {
            "ticket_id": ticket['id'],
            "response_text": response_text,
            "department": department,
            "response_type": "automated" if priority in [Priority.LOW, Priority.MEDIUM] else "human_review_needed",
            "confidence": 0.88  # Simulated confidence
        }
        
        log_agent_action("RESPONSE", "Response generated", {"ticket_id": ticket['id'], "type": response['response_type']})
        
        return response
    
    def _create_response(self, content: str, category: str, priority: str, department: str) -> str:
        """
        Create response text based on ticket details
        
        Args:
            content: Original ticket content
            category: Ticket category
            priority: Ticket priority
            department: Assigned department
            
        Returns:
            Response text
        """
        # Base greeting
        greeting = "Thank you for contacting our support team."
        
        # Category-specific responses
        if category == TicketCategory.TECHNICAL:
            body = self._technical_response(priority)
        elif category == TicketCategory.BILLING:
            body = self._billing_response(priority)
        elif category == TicketCategory.ACCOUNT:
            body = self._account_response(priority)
        elif category == TicketCategory.FEATURE_REQUEST:
            body = self._feature_request_response()
        else:
            body = self._general_response()
        
        # Closing
        closing = self._get_closing(priority)
        
        return f"{greeting}\n\n{body}\n\n{closing}"
    
    def _technical_response(self, priority: str) -> str:
        """Generate technical support response"""
        if priority == Priority.URGENT:
            return ("We understand you're experiencing a critical technical issue. "
                   "Our technical team has been immediately notified and will investigate this with highest priority. "
                   "We'll provide an update within the next 2 hours.")
        else:
            return ("We've received your technical support request. "
                   "Our technical team is reviewing the issue and will provide a solution shortly. "
                   "In the meantime, please ensure you're using the latest version of our software.")
    
    def _billing_response(self, priority: str) -> str:
        """Generate billing support response"""
        return ("We've received your billing inquiry. "
               "Our billing team is reviewing your account and will provide a detailed response within 24 hours. "
               "If you have any immediate concerns, please don't hesitate to reach out.")
    
    def _account_response(self, priority: str) -> str:
        """Generate account support response"""
        return ("We're here to help with your account issue. "
               "Our customer success team is looking into this and will assist you in resolving it. "
               "For security purposes, we may need to verify your identity before making any account changes.")
    
    def _feature_request_response(self) -> str:
        """Generate feature request response"""
        return ("Thank you for your feature suggestion! "
               "We truly value customer feedback as it helps us improve our product. "
               "Your request has been forwarded to our product team for consideration in future updates.")
    
    def _general_response(self) -> str:
        """Generate general inquiry response"""
        return ("We've received your inquiry and our customer success team is reviewing it. "
               "We'll provide you with a comprehensive response shortly.")
    
    def _get_closing(self, priority: str) -> str:
        """Get appropriate closing based on priority"""
        if priority == Priority.URGENT:
            return ("This ticket has been marked as urgent and is receiving immediate attention.\n\n"
                   "Best regards,\n"
                   "Customer Support Team")
        else:
            return ("If you have any additional questions, please feel free to reply to this ticket.\n\n"
                   "Best regards,\n"
                   "Customer Support Team")
