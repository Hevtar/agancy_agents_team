"""
Social Media Manager Agent - Manages social media presence and campaigns.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class SocialMediaManagerAgent(BaseAgent):
    """
    Social Media Manager Agent responsible for:
    - Social media strategy and planning
    - Content creation for social platforms
    - Community management
    - Social media advertising
    - Influencer outreach
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an experienced Social Media Manager with expertise in building brand presence across social platforms.
Your role is to create engaging social media strategies and content that drives community growth and engagement.

Key responsibilities:
1. Develop social media strategies aligned with brand goals
2. Create platform-specific content calendars
3. Write engaging posts optimized for each platform
4. Manage community interactions and responses
5. Plan and execute social media campaigns
6. Analyze performance and optimize strategies

You are creative, trend-aware, and understand social media algorithms.
You know how to create content that resonates with different audiences on each platform.

When creating social media content:
- Understand each platform's unique characteristics
- Adapt tone and style to the platform
- Use relevant hashtags strategically
- Create content that encourages engagement
- Maintain brand voice and consistency
- Plan for optimal posting times
- Include visual content recommendations
- Monitor trends and current events

You excel at building engaged communities and driving social ROI."""
        
        super().__init__(
            name="social_media_manager",
            role="Social Media Manager",
            goal="Build and engage social media communities across platforms",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def create_social_media_strategy(self, business_goals: List[str], target_audience: Dict, platforms: List[str]) -> Dict[str, Any]:
        """Create a comprehensive social media strategy."""
        prompt = f"""Develop a social media strategy:

Business Goals: {', '.join(business_goals)}
Target Audience: {target_audience}
Platforms: {', '.join(platforms)}

Provide:
1. Platform-specific strategies
2. Content pillars and themes
3. Posting frequency and timing
4. Community management approach
5. Influencer collaboration strategy
6. Paid social recommendations
7. Success metrics and KPIs
8. Content mix (organic vs promotional)"""
        
        return await self.execute(prompt)
    
    async def create_content_calendar(self, strategy: Dict, timeframe: str = "1 month") -> Dict[str, Any]:
        """Create a social media content calendar."""
        prompt = f"""Create a social media content calendar:

Strategy: {strategy}
Timeframe: {timeframe}

Provide:
1. Daily posting schedule
2. Content topics and themes
3. Platform-specific post variations
4. Hashtag strategies
5. Visual content requirements
6. Engagement prompts
7. Campaign integration
8. Key dates and events"""
        
        return await self.execute(prompt)
    
    async def write_social_posts(self, topic: str, platforms: List[str], tone: str = "engaging", count: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """Write social media posts for multiple platforms."""
        prompt = f"""Write {count} social media posts for each platform:

Topic: {topic}
Platforms: {', '.join(platforms)}
Tone: {tone}

For each platform provide:
- Platform-optimized content
- Character count compliance
- Relevant hashtags
- Engagement hooks
- Visual content suggestions
- Call-to-action

Adapt content style to each platform's best practices."""
        
        return await self.execute(prompt)
    
    async def analyze_social_performance(self, metrics: Dict, goals: Dict) -> Dict[str, Any]:
        """Analyze social media performance and provide recommendations."""
        prompt = f"""Analyze social media performance:

Metrics: {metrics}
Goals: {goals}

Provide:
1. Performance summary by platform
2. Top performing content analysis
3. Engagement rate analysis
4. Audience growth insights
5. Content recommendations
6. Optimal posting times
7. Hashtag performance
8. Competitive analysis
9. Improvement opportunities"""
        
        return await self.execute(prompt)
    
    async def create_influencer_outreach(self, campaign_goals: str, target_audience: str, budget: Optional[float] = None) -> Dict[str, Any]:
        """Create an influencer outreach strategy."""
        prompt = f"""Create an influencer outreach strategy:

Campaign Goals: {campaign_goals}
Target Audience: {target_audience}
Budget: {budget if budget else 'To be determined'}

Provide:
1. Influencer criteria and selection guidelines
2. Outreach approach and messaging
3. Collaboration types and compensation
4. Campaign brief template
5. Performance tracking metrics
6. Legal and compliance considerations
7. Relationship management approach"""
        
        return await self.execute(prompt)


# Singleton instance
_social_media_manager_instance = None

def get_social_media_manager_agent(memory: Optional[AgentMemory] = None, **kwargs) -> SocialMediaManagerAgent:
    """Get or create the Social Media Manager agent instance."""
    global _social_media_manager_instance
    if _social_media_manager_instance is None:
        _social_media_manager_instance = SocialMediaManagerAgent(memory=memory, **kwargs)
    return _social_media_manager_instance