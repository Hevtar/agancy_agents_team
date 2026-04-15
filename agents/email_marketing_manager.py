"""
Email Marketing Manager Agent - Email campaign specialist.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class EmailMarketingManagerAgent(BaseAgent):
    """
    Email Marketing Manager Agent responsible for:
    - Email campaign strategy and planning
    - Email copywriting and design
    - List segmentation and personalization
    - Automation workflow creation
    - Email performance analysis
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an Email Marketing Manager with expertise in creating high-converting email campaigns.
Your role is to develop email strategies that nurture leads and drive customer engagement.

Key responsibilities:
1. Develop email marketing strategies
2. Create compelling email content
3. Design automation workflows
4. Segment email lists
5. A/B test email elements
6. Analyze email performance metrics

You are strategic, creative, and data-driven.
You understand email deliverability and best practices.

When creating email campaigns:
- Focus on clear objectives and CTAs
- Personalize content for segments
- Optimize for mobile devices
- Test subject lines and content
- Monitor deliverability metrics
- Follow email marketing regulations

You excel at turning subscribers into customers."""
        
        super().__init__(
            name="email_marketing_manager",
            role="Email Marketing Manager",
            goal="Create email campaigns that nurture leads and drive conversions",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def create_email_strategy(self, business_goals: List[str], target_audience: Dict, email_frequency: str) -> Dict[str, Any]:
        """Create comprehensive email marketing strategy."""
        prompt = f"""Develop an email marketing strategy:

Business Goals: {', '.join(business_goals)}
Target Audience: {target_audience}
Email Frequency: {email_frequency}

Provide:
1. Email types and purposes
2. Segmentation strategy
3. Content calendar
4. Automation workflows
5. Personalization approach
6. Success metrics
7. Compliance considerations"""
        
        return await self.execute(prompt)
    
    async def write_email_campaign(self, campaign_type: str, target_segment: str, offer: str, brand_voice: str = "professional") -> Dict[str, Any]:
        """Write email campaign content."""
        prompt = f"""Write an email campaign:

Campaign Type: {campaign_type}
Target Segment: {target_segment}
Offer: {offer}
Brand Voice: {brand_voice}

Provide:
1. Subject line options (A/B test variants)
2. Preheader text
3. Email body content
4. CTA recommendations
5. Personalization tokens
6. Mobile optimization notes
7. Unsubscribe compliance"""
        
        return await self.execute(prompt)
    
    async def create_automation_workflow(self, trigger_event: str, workflow_goal: str, steps: int = 3) -> Dict[str, Any]:
        """Create email automation workflow."""
        prompt = f"""Create an email automation workflow:

Trigger Event: {trigger_event}
Workflow Goal: {workflow_goal}
Number of Steps: {steps}

Provide:
1. Workflow diagram and logic
2. Email sequence content
3. Timing and delays
4. Conditional branching
5. Exit criteria
6. Success metrics
7. Optimization opportunities"""
        
        return await self.execute(prompt)


# Singleton instance
_email_marketing_manager_instance = None

def get_email_marketing_manager_agent(memory: Optional[AgentMemory] = None, **kwargs) -> EmailMarketingManagerAgent:
    """Get or create the Email Marketing Manager agent instance."""
    global _email_marketing_manager_instance
    if _email_marketing_manager_instance is None:
        _email_marketing_manager_instance = EmailMarketingManagerAgent(memory=memory, **kwargs)
    return _email_marketing_manager_instance