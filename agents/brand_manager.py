"""
Brand Manager Agent - Brand strategy and identity expert.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class BrandManagerAgent(BaseAgent):
    """
    Brand Manager Agent responsible for:
    - Brand strategy development
    - Brand identity and guidelines
    - Brand positioning and messaging
    - Brand consistency across channels
    - Brand performance monitoring
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a Brand Manager with expertise in building and maintaining strong brand identities.
Your role is to ensure brand consistency and strengthen brand equity across all touchpoints.

Key responsibilities:
1. Develop brand strategies and positioning
2. Create brand guidelines and standards
3. Ensure brand consistency across channels
4. Monitor brand performance and perception
5. Manage brand assets and identity
6. Guide creative development

You are strategic, creative, and detail-oriented.
You understand brand psychology and consumer behavior.

When developing brand strategy:
- Start with brand purpose and values
- Understand target audience deeply
- Analyze competitive landscape
- Define unique brand positioning
- Create compelling brand stories
- Ensure consistency across touchpoints
- Measure and optimize brand health

You excel at building brands that connect with people and drive business growth."""
        
        super().__init__(
            name="brand_manager",
            role="Brand Manager",
            goal="Build and maintain strong brand identity and equity",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def develop_brand_strategy(self, company_values: List[str], target_audience: Dict, competitive_landscape: Dict) -> Dict[str, Any]:
        """Develop comprehensive brand strategy."""
        prompt = f"""Develop a brand strategy:

Company Values: {', '.join(company_values)}
Target Audience: {target_audience}
Competitive Landscape: {competitive_landscape}

Provide:
1. Brand purpose and mission
2. Brand vision and aspirations
3. Brand positioning statement
4. Brand personality and voice
5. Brand promise and value proposition
6. Brand story and narrative
7. Competitive differentiation
8. Brand architecture (if applicable)
9. Brand activation recommendations"""
        
        return await self.execute(prompt)
    
    async def create_brand_guidelines(self, brand_strategy: Dict, visual_elements: Optional[Dict] = None) -> Dict[str, Any]:
        """Create comprehensive brand guidelines."""
        prompt = f"""Create brand guidelines:

Brand Strategy: {brand_strategy}
Visual Elements: {visual_elements or 'To be developed'}

Provide:
1. Brand story and messaging framework
2. Voice and tone guidelines
3. Logo usage and clearspace
4. Color palette and applications
5. Typography system
6. Imagery and photography style
7. Iconography and graphics
8. Layout and composition principles
9. Application examples
10. Dos and don'ts
11. Digital and print specifications"""
        
        return await self.execute(prompt)
    
    async def audit_brand_consistency(self, brand_touchpoints: List[Dict], brand_guidelines: Dict) -> Dict[str, Any]:
        """Audit brand consistency across touchpoints."""
        prompt = f"""Audit brand consistency:

Brand Touchpoints: {brand_touchpoints}
Brand Guidelines: {brand_guidelines}

Provide:
1. Consistency assessment by touchpoint
2. Brand compliance score
3. Areas of inconsistency
4. Brand dilution risks
5. Improvement recommendations
6. Priority action items
7. Brand governance suggestions"""
        
        return await self.execute(prompt)
    
    async def develop_messaging_framework(self, brand_positioning: str, target_audience: Dict, key_messages: List[str]) -> Dict[str, Any]:
        """Develop a messaging framework."""
        prompt = f"""Develop messaging framework:

Brand Positioning: {brand_positioning}
Target Audience: {target_audience}
Key Messages: {', '.join(key_messages)}

Provide:
1. Brand tagline options
2. Elevator pitch
3. Value proposition statements
4. Message hierarchy
5. Audience-specific messaging
6. Channel-specific adaptations
7. Proof points and support
8. Tone and voice examples
9. Messaging dos and don'ts"""
        
        return await self.execute(prompt)


# Singleton instance
_brand_manager_instance = None

def get_brand_manager_agent(memory: Optional[AgentMemory] = None, **kwargs) -> BrandManagerAgent:
    """Get or create the Brand Manager agent instance."""
    global _brand_manager_instance
    if _brand_manager_instance is None:
        _brand_manager_instance = BrandManagerAgent(memory=memory, **kwargs)
    return _brand_manager_instance