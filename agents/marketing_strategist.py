"""
Marketing Strategist Agent - Develops comprehensive marketing strategies.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class MarketingStrategistAgent(BaseAgent):
    """
    Marketing Strategist Agent responsible for:
    - Developing comprehensive marketing strategies
    - Market analysis and competitive intelligence
    - Campaign planning and optimization
    - Brand positioning and messaging
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a Senior Marketing Strategist with 10+ years of experience in digital marketing.
Your role is to develop data-driven marketing strategies that achieve business objectives.

Key responsibilities:
1. Analyze market trends and competitive landscape
2. Define target audiences and buyer personas
3. Create comprehensive marketing strategies
4. Develop campaign concepts and messaging
5. Recommend channels and tactics
6. Set KPIs and success metrics

You are analytical, creative, and strategic.
You base recommendations on data and proven marketing principles.

When developing strategies:
- Start with clear business objectives
- Analyze the target market and competition
- Identify unique value propositions
- Create integrated multi-channel approaches
- Define measurable success criteria
- Consider budget and resource constraints

You excel at turning complex market data into actionable strategies."""
        
        super().__init__(
            name="marketing_strategist",
            role="Marketing Strategist",
            goal="Develop data-driven marketing strategies that achieve business objectives",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def analyze_market(self, industry: str, target_market: str, competitors: List[str]) -> Dict[str, Any]:
        """Analyze market conditions and competitive landscape."""
        prompt = f"""Conduct a comprehensive market analysis:

Industry: {industry}
Target Market: {target_market}
Key Competitors: {', '.join(competitors)}

Provide:
1. Market size and growth trends
2. Key market drivers and challenges
3. Competitive analysis (strengths/weaknesses)
4. Market opportunities and threats
5. Recommended positioning strategy"""
        
        return await self.execute(prompt)
    
    async def develop_strategy(self, business_goals: List[str], target_audience: Dict, budget: Optional[float] = None) -> Dict[str, Any]:
        """Develop a comprehensive marketing strategy."""
        prompt = f"""Develop a marketing strategy based on:

Business Goals: {', '.join(business_goals)}
Target Audience: {target_audience}
Budget: {budget if budget else 'To be determined'}

Provide:
1. Strategic approach and key messages
2. Recommended marketing channels
3. Campaign concepts and themes
4. Content strategy recommendations
5. Timeline and milestones
6. KPIs and measurement framework
7. Budget allocation recommendations"""
        
        return await self.execute(prompt)
    
    async def create_campaign_plan(self, campaign_objective: str, target_audience: str, channels: List[str]) -> Dict[str, Any]:
        """Create a detailed campaign plan."""
        prompt = f"""Create a detailed campaign plan:

Campaign Objective: {campaign_objective}
Target Audience: {target_audience}
Channels: {', '.join(channels)}

Provide:
1. Campaign concept and messaging
2. Channel-specific tactics
3. Content requirements
4. Timeline and schedule
5. Budget breakdown
6. Success metrics and tracking plan"""
        
        return await self.execute(prompt)
    
    async def optimize_campaign(self, current_performance: Dict, goals: Dict) -> Dict[str, Any]:
        """Analyze campaign performance and recommend optimizations."""
        prompt = f"""Optimize this marketing campaign:

Current Performance: {current_performance}
Campaign Goals: {goals}

Provide:
1. Performance analysis (what's working/not working)
2. Specific optimization recommendations
3. A/B testing suggestions
4. Budget reallocation recommendations
5. Expected impact of optimizations"""
        
        return await self.execute(prompt)


# Singleton instance
_marketing_strategist_instance = None

def get_marketing_strategist_agent(memory: Optional[AgentMemory] = None, **kwargs) -> MarketingStrategistAgent:
    """Get or create the Marketing Strategist agent instance."""
    global _marketing_strategist_instance
    if _marketing_strategist_instance is None:
        _marketing_strategist_instance = MarketingStrategistAgent(memory=memory, **kwargs)
    return _marketing_strategist_instance