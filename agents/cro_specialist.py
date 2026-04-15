"""
CRO Specialist Agent - Conversion rate optimization expert.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class CROSpecialistAgent(BaseAgent):
    """
    CRO Specialist Agent responsible for:
    - Conversion funnel analysis
    - A/B test design and analysis
    - Landing page optimization
    - User behavior analysis
    - Checkout optimization
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a CRO Specialist with expertise in optimizing conversion rates.
Your role is to systematically improve conversion rates through data-driven testing and optimization.

Key responsibilities:
1. Analyze conversion funnels and identify drop-off points
2. Design and analyze A/B tests
3. Optimize landing pages and checkout flows
4. Analyze user behavior and heatmaps
5. Develop conversion hypotheses
6. Implement and measure optimization changes

You are analytical, methodical, and results-driven.
You understand user psychology and persuasion principles.

When optimizing conversions:
- Start with data analysis and user research
- Formulate clear, testable hypotheses
- Prioritize tests by potential impact
- Ensure statistical significance
- Consider the entire user journey
- Balance short-term gains with long-term brand health
- Document learnings and iterate

You excel at turning visitors into customers through systematic optimization."""
        
        super().__init__(
            name="cro_specialist",
            role="CRO Specialist",
            goal="Systematically improve conversion rates through testing and optimization",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def analyze_conversion_funnel(self, funnel_data: Dict, traffic_sources: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze conversion funnel and identify optimization opportunities."""
        prompt = f"""Analyze conversion funnel:

Funnel Data: {funnel_data}
Traffic Sources: {traffic_sources or 'Not specified'}

Provide:
1. Funnel visualization and drop-off analysis
2. Conversion rate by stage
3. Bottleneck identification
4. Traffic source performance
5. User behavior patterns
6. Hypothesis generation
7. Prioritized optimization opportunities
8. Expected impact estimates"""
        
        return await self.execute(prompt)
    
    async def design_ab_test(self, hypothesis: str, current_performance: Dict, test_elements: List[str]) -> Dict[str, Any]:
        """Design an A/B test with proper methodology."""
        prompt = f"""Design an A/B test:

Hypothesis: {hypothesis}
Current Performance: {current_performance}
Test Elements: {', '.join(test_elements)}

Provide:
1. Test design and methodology
2. Variation descriptions
3. Sample size calculation
4. Test duration estimation
5. Success metrics and KPIs
6. Statistical significance requirements
7. Implementation guidelines
8. Analysis plan
9. Risk assessment and mitigation"""
        
        return await self.execute(prompt)
    
    async def optimize_landing_page(self, page_data: Dict, target_action: str, traffic_type: str) -> Dict[str, Any]:
        """Optimize landing page for conversions."""
        prompt = f"""Optimize landing page:

Page Data: {page_data}
Target Action: {target_action}
Traffic Type: {traffic_type}

Provide:
1. Page audit and heuristic analysis
2. Headline and copy optimization
3. CTA optimization
4. Form optimization (if applicable)
5. Visual hierarchy improvements
6. Trust element recommendations
7. Mobile optimization
8. Page speed considerations
9. A/B test recommendations
10. Expected conversion lift"""
        
        return await self.execute(prompt)
    
    async def analyze_user_behavior(self, analytics_data: Dict, heatmap_data: Optional[Dict] = None, session_recordings: Optional[List] = None) -> Dict[str, Any]:
        """Analyze user behavior to identify optimization opportunities."""
        prompt = f"""Analyze user behavior:

Analytics Data: {analytics_data}
Heatmap Data: {heatmap_data or 'Not available'}
Session Recordings: {session_recordings or 'Not available'}

Provide:
1. User behavior patterns
2. Engagement analysis
3. Friction point identification
4. UX issues and opportunities
5. Content effectiveness
6. Navigation analysis
7. Mobile vs desktop differences
8. Optimization recommendations
9. Hypothesis generation for testing"""
        
        return await self.execute(prompt)


# Singleton instance
_cro_specialist_instance = None

def get_cro_specialist_agent(memory: Optional[AgentMemory] = None, **kwargs) -> CROSpecialistAgent:
    """Get or create the CRO Specialist agent instance."""
    global _cro_specialist_instance
    if _cro_specialist_instance is None:
        _cro_specialist_instance = CROSpecialistAgent(memory=memory, **kwargs)
    return _cro_specialist_instance