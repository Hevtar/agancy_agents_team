"""
UX Designer Agent - User experience and interface design expert.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class UXDesignerAgent(BaseAgent):
    """
    UX Designer Agent responsible for:
    - User research and persona development
    - Wireframing and prototyping
    - User journey mapping
    - Usability analysis and recommendations
    - Conversion rate optimization
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a UX Designer with expertise in creating user-centered digital experiences.
Your role is to ensure products are intuitive, accessible, and optimized for conversion.

Key responsibilities:
1. Conduct user research and create personas
2. Design wireframes and prototypes
3. Map user journeys and flows
4. Perform usability analysis
5. Optimize for conversion and user satisfaction
6. Ensure accessibility compliance

You are user-focused, creative, and detail-oriented.
You understand design principles and conversion optimization.

When designing experiences:
- Start with user needs and goals
- Follow accessibility guidelines
- Create intuitive navigation
- Optimize for mobile-first
- Test and iterate based on feedback
- Balance aesthetics with functionality

You excel at creating experiences that users love and that drive business results."""
        
        super().__init__(
            name="ux_designer",
            role="UX Designer",
            goal="Create user-centered designs that optimize experience and conversion",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def create_user_personas(self, target_market: str, product_type: str, research_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Create detailed user personas."""
        prompt = f"""Create user personas:

Target Market: {target_market}
Product Type: {product_type}
Research Data: {research_data or 'Based on typical user patterns'}

Provide:
1. 3-4 detailed personas
2. Demographics and background
3. Goals and motivations
4. Pain points and challenges
5. Behavior patterns
6. Technology usage
7. Quotes and scenarios
8. Design implications for each persona"""
        
        return await self.execute(prompt)
    
    async def create_user_journey_map(self, persona: Dict, goal: str, touchpoints: List[str]) -> Dict[str, Any]:
        """Create a comprehensive user journey map."""
        prompt = f"""Create a user journey map:

Persona: {persona}
Goal: {goal}
Touchpoints: {', '.join(touchpoints)}

Provide:
1. Journey stages
2. User actions at each stage
3. Thoughts and emotions
4. Pain points and opportunities
5. Channel interactions
6. Moments of truth
7. Improvement recommendations
8. Success metrics for each stage"""
        
        return await self.execute(prompt)
    
    async def design_wireframe(self, page_type: str, user_goals: List[str], business_goals: List[str], content_requirements: List[str]) -> Dict[str, Any]:
        """Create wireframe specifications."""
        prompt = f"""Design wireframe specifications:

Page Type: {page_type}
User Goals: {', '.join(user_goals)}
Business Goals: {', '.join(business_goals)}
Content Requirements: {', '.join(content_requirements)}

Provide:
1. Layout structure and hierarchy
2. Component placement and sizing
3. Navigation elements
4. Content areas and CTAs
5. Form fields and interactions
6. Mobile responsiveness considerations
7. Accessibility requirements
8. User flow connections"""
        
        return await self.execute(prompt)
    
    async def perform_usability_analysis(self, current_design: Dict, user_feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        """Perform usability analysis and provide recommendations."""
        prompt = f"""Perform usability analysis:

Current Design: {current_design}
User Feedback: {user_feedback or 'No feedback available'}

Provide:
1. Usability heuristic evaluation
2. Accessibility compliance check
3. User flow analysis
4. Pain point identification
5. Conversion optimization opportunities
6. Specific improvement recommendations
7. Priority ranking of issues
8. Testing recommendations"""
        
        return await self.execute(prompt)


# Singleton instance
_ux_designer_instance = None

def get_ux_designer_agent(memory: Optional[AgentMemory] = None, **kwargs) -> UXDesignerAgent:
    """Get or create the UX Designer agent instance."""
    global _ux_designer_instance
    if _ux_designer_instance is None:
        _ux_designer_instance = UXDesignerAgent(memory=memory, **kwargs)
    return _ux_designer_instance