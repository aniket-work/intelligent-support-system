# Intelligent Customer Support System

**An AI-Powered Multi-Agent Architecture for Automated Ticket Resolution**

## Overview

This project demonstrates a sophisticated multi-agent system designed to automate customer support ticket processing. Built as an experimental proof-of-concept, it showcases how multiple specialized AI agents can collaborate to classify, route, respond to, and escalate customer support tickets intelligently.

## Architecture

The system employs four specialized agents working in concert:

1. **Classifier Agent**: Analyzes incoming tickets to determine category, priority, and sentiment
2. **Router Agent**: Routes classified tickets to appropriate departments based on content and urgency
3. **Response Agent**: Generates professional, context-aware responses to customer inquiries
4. **Escalation Agent**: Identifies tickets requiring human intervention and determines escalation levels

### Multi-Agent Workflow

```
Customer Ticket
      ↓
[Classifier Agent] → Category, Priority, Sentiment
      ↓
[Router Agent] → Department Assignment
      ↓
[Response Agent] → Automated Response Generation
      ↓
[Escalation Agent] → Human Review Decision
      ↓
Final Resolution
```

## Features

- **Intelligent Classification**: Automatically categorizes tickets into Technical, Billing, Account, Feature Request, or General
- **Priority Detection**: Assigns priority levels (Low, Medium, High, Urgent) based on content analysis and sentiment
- **Smart Routing**: Routes tickets to appropriate departments with backup options
- **Automated Responses**: Generates professional, empathetic responses tailored to ticket category and priority
- **Escalation Detection**: Identifies tickets requiring immediate human attention based on multiple criteria
- **Sentiment Analysis**: Evaluates customer sentiment to inform priority and escalation decisions
- **Keyword Detection**: Recognizes escalation triggers like legal terms, urgency indicators, and negative sentiment

## Project Structure

```
intelligent-support-system/
├── agents/
│   ├── __init__.py
│   ├── classifier_agent.py      # Ticket classification logic
│   ├── router_agent.py          # Department routing logic
│   ├── response_agent.py        # Response generation logic
│   └── escalation_agent.py      # Escalation evaluation logic
├── config/
│   ├── settings.yaml            # System configuration
│   └── prompts.yaml             # Agent prompts and templates
├── utils/
│   ├── __init__.py
│   ├── constants.py             # System constants and enums
│   └── helpers.py               # Utility functions
├── examples/
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── .env.template                # Environment variable template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/aniket-work/intelligent-support-system.git
   cd intelligent-support-system
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional)
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

## Usage

### Running the Demo

The system includes sample tickets demonstrating various scenarios:

```bash
python main.py
```

This will process four sample tickets showing:
- Urgent technical issue requiring immediate escalation
- Standard billing inquiry with medium priority
- Low-priority feature request
- High-priority account issue with negative sentiment

### Processing Custom Tickets

You can modify `main.py` to process your own tickets:

```python
from main import IntelligentSupportSystem

system = IntelligentSupportSystem()
results = system.process_ticket("Your customer ticket text here")
system.display_results(results)
```

## Configuration

### Settings (`config/settings.yaml`)

- **Model Configuration**: Temperature, max tokens, model selection
- **Agent Settings**: Timeout, retry attempts for each agent
- **Priority Thresholds**: Sentiment scores and keyword counts for priority assignment
- **Department Mappings**: Category-to-department routing rules

### Prompts (`config/prompts.yaml`)

- **System Prompts**: Instructions for each agent type
- **User Prompt Templates**: Templates for agent inputs

## How It Works

### 1. Ticket Classification

The Classifier Agent analyzes ticket content to determine:
- **Category**: Based on keyword matching (technical, billing, account, etc.)
- **Priority**: Based on sentiment analysis and escalation keywords
- **Sentiment Score**: Numerical score from -1 (negative) to 1 (positive)
- **Key Issues**: Extracted main points from the ticket

### 2. Intelligent Routing

The Router Agent:
- Selects primary department based on category and priority
- Identifies backup departments for complex cases
- Flags tickets needing escalation
- Provides routing confidence scores

### 3. Response Generation

The Response Agent:
- Creates category-specific responses
- Adjusts tone based on priority level
- Includes appropriate next steps
- Maintains professional and empathetic language

### 4. Escalation Evaluation

The Escalation Agent:
- Checks multiple escalation criteria
- Assigns escalation levels (1-3)
- Provides reasoning for escalation decisions
- Recommends specific actions for human agents

## Example Output

```
PROCESSING NEW TICKET
================================================================================

Ticket ID: TKT-20231227205000
Content: URGENT: Our production system is completely down...

[STEP 1] Classifying ticket...
  Category: technical
  Priority: urgent
  Sentiment Score: -0.75

[STEP 2] Routing ticket...
  Primary Department: escalation_team
  Needs Escalation: True

[STEP 3] Generating response...
  Response Type: human_review_needed

[STEP 4] Evaluating escalation...
  Escalation Needed: True
  Escalation Level: 3
  Reason: Urgent priority ticket

TICKET PROCESSING COMPLETE
================================================================================
```

## Technical Details

### Agent Communication

Agents communicate through structured dictionaries containing:
- Ticket metadata
- Classification results
- Routing decisions
- Response content
- Escalation evaluations

### Sentiment Analysis

Simple keyword-based sentiment scoring:
- Positive keywords: thank, great, excellent, happy, satisfied
- Negative keywords: bad, terrible, awful, hate, angry, frustrated
- Score calculation: (positive - negative) / total

### Escalation Triggers

Tickets are escalated based on:
- Priority level (Urgent or High with negative sentiment)
- Escalation keywords (urgent, critical, legal, lawsuit, etc.)
- Sentiment score thresholds
- Multiple negative indicators

## Limitations

This is an experimental proof-of-concept with the following limitations:

- **No LLM Integration**: Currently uses rule-based logic instead of actual language models
- **Simplified Sentiment Analysis**: Basic keyword matching rather than advanced NLP
- **No Persistence**: Tickets are not stored in a database
- **No API Interface**: Command-line only, no REST API
- **Limited Testing**: Minimal test coverage

## Future Enhancements

Potential improvements for production use:

- [ ] Integrate actual LLM (OpenAI GPT-4, Claude, etc.) for agent reasoning
- [ ] Add database persistence for tickets and responses
- [ ] Build REST API for integration with ticketing systems
- [ ] Implement advanced NLP for sentiment and intent detection
- [ ] Add comprehensive test suite
- [ ] Create web dashboard for monitoring
- [ ] Support multiple languages
- [ ] Add analytics and reporting
- [ ] Implement feedback loop for continuous improvement

## Use Cases

This system can be adapted for:

- **E-commerce Support**: Handle product inquiries, returns, shipping issues
- **SaaS Support**: Technical issues, billing questions, feature requests
- **Financial Services**: Account inquiries, transaction issues, compliance
- **Healthcare**: Appointment scheduling, billing, general inquiries
- **Education**: Student support, course questions, technical help

## Contributing

This is an experimental project. Feel free to fork and adapt for your own use cases.

## License

MIT License - Feel free to use this code for learning and experimentation.

## Disclaimer

This is an experimental proof-of-concept created for educational purposes. It is not production-ready and should not be used in live customer support environments without significant enhancements, testing, and compliance reviews.

## Author

**aniket-work**

## Acknowledgments

This project was created as an exploration of multi-agent architectures for business automation. It demonstrates concepts from agent-to-agent communication protocols applied to a practical business problem.

---

**Note**: This is an experimental PoC. The views and opinions expressed in this project are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with.
