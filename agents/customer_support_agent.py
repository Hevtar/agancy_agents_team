"""
Customer Support Agent - Customer service and support specialist.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class CustomerSupportAgent(BaseAgent):
    """
    Customer Support Agent responsible for:
    - Customer inquiry handling
    - Issue resolution and escalation
    - Support documentation creation
    - Customer satisfaction monitoring
    - FAQ and knowledge base management
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a Customer Support Specialist with expertise in providing exceptional customer service.
Your role is to resolve customer issues efficiently while maintaining high satisfaction levels.

Key responsibilities:
1. Handle customer inquiries across channels
2. Resolve issues and complaints
3. Create support documentation
4. Monitor customer satisfaction
5. Escalate complex issues appropriately
6. Maintain knowledge base and FAQs

You are empathetic, patient, and solution-oriented.
You excel at turning frustrated customers into satisfied advocates.

When handling customer issues:
- Listen actively and show empathy
- Understand the root cause
- Provide clear, actionable solutions
- Follow up to ensure resolution
- Document learnings for future reference
- Escalate when necessary
- Maintain professional tone

You excel at providing support that builds customer loyalty."""
        
        super().__init__(
            name="customer_support_agent",
            role="Customer Support Specialist",
            goal="Provide exceptional customer support that builds loyalty and satisfaction",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def handle_inquiry(self, inquiry_type: str, customer_message: str, customer_history: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle customer inquiry with appropriate response."""
        prompt = f"""Handle customer inquiry:

Inquiry Type: {inquiry_type}
Customer Message: {customer_message}
Customer History: {customer_history or 'New customer'}

Provide:
1. Empathetic acknowledgment
2. Clear response to inquiry
3. Solution or next steps
4. Timeline expectations
5. Follow-up actions
6. Escalation if needed
7. Customer satisfaction check"""
        
        return await self.execute(prompt)
    
    async def resolve_complaint(self, complaint_details: str, customer_value: str, previous_attempts: Optional[List] = None) -> Dict[str, Any]:
        """Resolve customer complaint effectively."""
        prompt = f"""Resolve customer complaint:

Complaint Details: {complaint_details}
Customer Value: {customer_value}
Previous Attempts: {previous_attempts or 'First attempt'}

Provide:
1. Empathetic acknowledgment and apology
2. Root cause analysis
3. Resolution proposal
4. Compensation or goodwill gesture (if appropriate)
5. Prevention measures
6. Follow-up plan
7. Escalation path if unresolved"""
        
        return await self.execute(prompt)
    
    async def create_support_documentation(self, topic: str, target_audience: str, complexity: str = "intermediate") -> Dict[str, Any]:
        """Create customer support documentation."""
        prompt = f"""Create support documentation:

Topic: {topic}
Target Audience: {target_audience}
Complexity: {complexity}

Provide:
1. Clear, step-by-step instructions
2. Screenshots or visual aids (descriptions)
3. Troubleshooting section
4. FAQ section
5. Related resources
6. Search-friendly structure
7. Accessibility considerations"""
        
        return await self.execute(prompt)
    
    async def analyze_support_metrics(self, metrics: Dict, goals: Dict, timeframe: str) -> Dict[str, Any]:
        """Analyze customer support performance metrics."""
        prompt = f"""Analyze support metrics:

Metrics: {metrics}
Goals: {goals}
Timeframe: {timeframe}

Provide:
1. Performance summary vs goals
2. Trend analysis
3. Customer satisfaction insights
4. Response time analysis
5. Resolution rate analysis
6. Common issue identification
7. Agent performance insights
8. Improvement recommendations
9. Resource allocation suggestions"""
        
        return await self.execute(prompt)


# Singleton instance
_customer_support_instance = None

def get_customer_support_agent(memory: Optional[AgentMemory] = None, **kwargs) -> CustomerSupportAgent:
    """Get or create the Customer Support agent instance."""
    global _customer_support_instance
    if _customer_support_instance is None:
        _customer_support_instance = CustomerSupportAgent(memory=memory, **kwargs)
    return _customer_support_instance