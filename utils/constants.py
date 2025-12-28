"""
Constants for the Intelligent Support System
"""

# Ticket Categories
class TicketCategory:
    TECHNICAL = "technical"
    BILLING = "billing"
    GENERAL = "general"
    ACCOUNT = "account"
    FEATURE_REQUEST = "feature_request"

# Priority Levels
class Priority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Department Names
class Department:
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_SUPPORT = "billing_support"
    CUSTOMER_SUCCESS = "customer_success"
    PRODUCT_TEAM = "product_team"
    ESCALATION_TEAM = "escalation_team"

# Ticket Status
class TicketStatus:
    NEW = "new"
    CLASSIFIED = "classified"
    ROUTED = "routed"
    RESPONDED = "responded"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"

# Agent Types
class AgentType:
    CLASSIFIER = "classifier"
    ROUTER = "router"
    RESPONSE_GENERATOR = "response_generator"
    ESCALATION_HANDLER = "escalation_handler"

# Escalation Triggers
ESCALATION_KEYWORDS = [
    "urgent", "critical", "emergency", "asap", "immediately",
    "lawsuit", "legal", "attorney", "lawyer", "sue",
    "cancel", "refund", "money back", "charge back",
    "angry", "frustrated", "disappointed", "terrible"
]

# Priority Scoring Weights
PRIORITY_WEIGHTS = {
    "keyword_match": 0.3,
    "sentiment_score": 0.3,
    "complexity_score": 0.2,
    "customer_tier": 0.2
}
