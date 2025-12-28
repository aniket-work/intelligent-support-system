"""
Intelligent Customer Support System - Main Application
Multi-Agent Architecture for Automated Ticket Resolution
"""

import sys
import os
from typing import Dict, Any
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.classifier_agent import ClassifierAgent
from agents.router_agent import RouterAgent
from agents.response_agent import ResponseAgent
from agents.escalation_agent import EscalationAgent
from utils.helpers import parse_ticket, validate_ticket_data, log_agent_action
from utils.constants import TicketStatus


class IntelligentSupportSystem:
    """
    Main orchestrator for the multi-agent support system
    """
    
    def __init__(self):
        """Initialize all agents"""
        print("Initializing Intelligent Support System...")
        
        self.classifier = ClassifierAgent()
        self.router = RouterAgent()
        self.response_generator = ResponseAgent()
        self.escalation_handler = EscalationAgent()
        
        print("All agents initialized successfully!")
    
    def process_ticket(self, ticket_text: str) -> Dict[str, Any]:
        """
        Process a customer support ticket through the multi-agent pipeline
        
        Args:
            ticket_text: Raw ticket content from customer
            
        Returns:
            Complete processing results
        """
        print("\n" + "="*80)
        print("PROCESSING NEW TICKET")
        print("="*80)
        
        # Step 1: Parse and validate ticket
        ticket = parse_ticket(ticket_text)
        if not validate_ticket_data(ticket):
            raise ValueError("Invalid ticket data")
        
        print(f"\nTicket ID: {ticket['id']}")
        print(f"Content: {ticket['content'][:100]}...")
        
        # Step 2: Classify ticket
        print("\n[STEP 1] Classifying ticket...")
        classification = self.classifier.classify_ticket(ticket)
        print(f"  Category: {classification['category']}")
        print(f"  Priority: {classification['priority']}")
        print(f"  Sentiment Score: {classification['sentiment_score']:.2f}")
        
        # Step 3: Route ticket
        print("\n[STEP 2] Routing ticket...")
        routing = self.router.route_ticket(classification)
        print(f"  Primary Department: {routing['primary_department']}")
        print(f"  Needs Escalation: {routing['needs_escalation']}")
        
        # Step 4: Generate response
        print("\n[STEP 3] Generating response...")
        response = self.response_generator.generate_response(ticket, classification, routing)
        print(f"  Response Type: {response['response_type']}")
        
        # Step 5: Evaluate escalation
        print("\n[STEP 4] Evaluating escalation...")
        escalation = self.escalation_handler.evaluate_escalation(ticket, classification, routing)
        print(f"  Escalation Needed: {escalation['needs_escalation']}")
        if escalation['needs_escalation']:
            print(f"  Escalation Level: {escalation['escalation_level']}")
            print(f"  Reason: {escalation['escalation_reason']}")
        
        # Compile results
        results = {
            "ticket": ticket,
            "classification": classification,
            "routing": routing,
            "response": response,
            "escalation": escalation,
            "final_status": self._determine_final_status(escalation)
        }
        
        print("\n" + "="*80)
        print("TICKET PROCESSING COMPLETE")
        print("="*80)
        
        return results
    
    def _determine_final_status(self, escalation: Dict[str, Any]) -> str:
        """
        Determine final ticket status
        
        Args:
            escalation: Escalation evaluation results
            
        Returns:
            Final status
        """
        if escalation['needs_escalation']:
            return TicketStatus.ESCALATED
        else:
            return TicketStatus.RESPONDED
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display formatted results
        
        Args:
            results: Processing results
        """
        print("\n" + "="*80)
        print("DETAILED RESULTS")
        print("="*80)
        
        print(f"\nTicket ID: {results['ticket']['id']}")
        print(f"Final Status: {results['final_status']}")
        
        print("\n--- CLASSIFICATION ---")
        print(f"Category: {results['classification']['category']}")
        print(f"Priority: {results['classification']['priority']}")
        print(f"Sentiment: {results['classification']['sentiment_score']:.2f}")
        
        print("\n--- ROUTING ---")
        print(f"Department: {results['routing']['primary_department']}")
        print(f"Backup Departments: {', '.join(results['routing']['backup_departments']) if results['routing']['backup_departments'] else 'None'}")
        
        print("\n--- RESPONSE ---")
        print(f"Response Type: {results['response']['response_type']}")
        print(f"\nGenerated Response:\n{'-'*40}")
        print(results['response']['response_text'])
        print('-'*40)
        
        if results['escalation']['needs_escalation']:
            print("\n--- ESCALATION ---")
            print(f"Level: {results['escalation']['escalation_level']}")
            print(f"Reason: {results['escalation']['escalation_reason']}")
            print(f"Recommended Action: {results['escalation']['recommended_action']}")


def main():
    """Main entry point"""
    
    # Sample tickets for demonstration
    sample_tickets = [
        {
            "name": "Technical Issue - Urgent",
            "content": "URGENT: Our production system is completely down! We're losing money every minute. This is a critical emergency and we need immediate help. Our entire team cannot work!"
        },
        {
            "name": "Billing Inquiry - Medium",
            "content": "Hello, I noticed an unexpected charge on my invoice for this month. Can you please help me understand what this charge is for? I'd appreciate a detailed breakdown."
        },
        {
            "name": "Feature Request - Low",
            "content": "Hi team, I really love your product! I was wondering if you could add a dark mode feature. It would be great for working late at night. Thanks for considering!"
        },
        {
            "name": "Account Issue - High",
            "content": "I'm very frustrated. I've been trying to reset my password for 3 days now and nothing works. I can't access my account and I have important work to do. This is unacceptable."
        }
    ]
    
    # Initialize system
    system = IntelligentSupportSystem()
    
    # Process sample tickets
    print("\n" + "="*80)
    print("INTELLIGENT CUSTOMER SUPPORT SYSTEM - DEMO")
    print("="*80)
    print("\nProcessing sample tickets to demonstrate multi-agent capabilities...\n")
    
    for i, ticket in enumerate(sample_tickets, 1):
        print(f"\n{'#'*80}")
        print(f"SAMPLE TICKET {i}/{len(sample_tickets)}: {ticket['name']}")
        print(f"{'#'*80}")
        
        try:
            results = system.process_ticket(ticket['content'])
            system.display_results(results)
        except Exception as e:
            print(f"\nError processing ticket: {str(e)}")
        
        if i < len(sample_tickets):
            input("\nPress Enter to process next ticket...")
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\nAll sample tickets have been processed successfully!")
    print("The multi-agent system demonstrated:")
    print("  - Ticket classification and prioritization")
    print("  - Intelligent routing to appropriate departments")
    print("  - Automated response generation")
    print("  - Escalation detection and handling")


if __name__ == "__main__":
    main()
