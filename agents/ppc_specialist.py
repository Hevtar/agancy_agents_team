"""
PPC Specialist Agent - Paid advertising expert.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class PPCSpecialistAgent(BaseAgent):
    """
    PPC Specialist Agent responsible for:
    - Paid search campaign management
    - Display and social advertising
    - Bid management and optimization
    - Ad copy creation and testing
    - Budget allocation and ROI optimization
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a PPC Specialist with expertise in managing paid advertising campaigns.
Your role is to maximize ROI through strategic bid management and ad optimization.

Key responsibilities:
1. Create and manage PPC campaigns
2. Conduct keyword research for paid search
3. Write compelling ad copy
4. Optimize bids and budgets
5. A/B test ad variations
6. Analyze campaign performance

You are analytical, strategic, and ROI-focused.
You understand bidding strategies and quality score optimization.

When managing PPC campaigns:
- Focus on keyword intent and relevance
- Optimize for quality score
- Test ad variations continuously
- Monitor and adjust bids strategically
- Track conversions and attribution
- Optimize landing page experience

You excel at driving qualified traffic and maximizing ROAS."""
        
        super().__init__(
            name="ppc_specialist",
            role="PPC Specialist",
            goal="Manage paid advertising campaigns that maximize ROI and drive conversions",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def create_ppc_campaign(self, campaign_goal: str, target_keywords: List[str], budget: float, platforms: List[str]) -> Dict[str, Any]:
        """Create a comprehensive PPC campaign."""
        prompt = f"""Create a PPC campaign:

Campaign Goal: {campaign_goal}
Target Keywords: {', '.join(target_keywords)}
Budget: ${budget}
Platforms: {', '.join(platforms)}

Provide:
1. Campaign structure and organization
2. Keyword strategy and match types
3. Ad group organization
4. Ad copy variations
5. Bid strategy recommendations
6. Budget allocation
7. Targeting options
8. Conversion tracking setup
9. Success metrics and KPIs"""
        
        return await self.execute(prompt)
    
    async def optimize_bids(self, campaign_data: Dict, performance_goals: Dict) -> Dict[str, Any]:
        """Optimize PPC bids for better performance."""
        prompt = f"""Optimize PPC bids:

Campaign Data: {campaign_data}
Performance Goals: {performance_goals}

Provide:
1. Bid adjustment recommendations
2. Keyword-level optimizations
3. Device bid adjustments
4. Location bid adjustments
5. Time-of-day optimizations
6. Budget reallocation suggestions
7. Expected impact on performance"""
        
        return await self.execute(prompt)
    
    async def write_ad_copy(self, product_service: str, target_audience: str, platform: str, count: int = 3) -> Dict[str, Any]:
        """Write PPC ad copy variations."""
        prompt = f"""Write {count} PPC ad copy variations:

Product/Service: {product_service}
Target Audience: {target_audience}
Platform: {platform}

For each variation provide:
- Headline options
- Description text
- Display URL
- Call-to-action
- Ad extensions recommendations
- Character count compliance"""
        
        return await self.execute(prompt)


# Singleton instance
_ppc_specialist_instance = None

def get_ppc_specialist_agent(memory: Optional[AgentMemory] = None, **kwargs) -> PPCSpecialistAgent:
    """Get or create the PPC Specialist agent instance."""
    global _ppc_specialist_instance
    if _ppc_specialist_instance is None:
        _ppc_specialist_instance = PPCSpecialistAgent(memory=memory, **kwargs)
    return _ppc_specialist_instance