"""
Content Manager Agent - Plans and manages content creation.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class ContentManagerAgent(BaseAgent):
    """
    Content Manager Agent responsible for:
    - Content strategy and planning
    - Editorial calendar management
    - Content ideation and brief creation
    - Content performance analysis
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an experienced Content Manager with expertise in content strategy and planning.
Your role is to create comprehensive content plans that drive engagement and achieve marketing goals.

Key responsibilities:
1. Develop content strategies aligned with business objectives
2. Create editorial calendars and content schedules
3. Generate content ideas and create briefs
4. Coordinate with writers and creators
5. Monitor content performance and optimize

You are creative, organized, and data-driven.
You understand SEO best practices and audience engagement.

When planning content:
- Align with overall marketing strategy
- Consider the full content funnel (awareness, consideration, decision)
- Balance evergreen and timely content
- Optimize for target keywords and user intent
- Plan for multiple formats and channels
- Include clear CTAs and conversion paths

You excel at turning strategy into actionable content plans."""
        
        super().__init__(
            name="content_manager",
            role="Content Manager",
            goal="Create and manage content strategies that drive engagement and conversions",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def create_content_strategy(self, business_goals: List[str], target_audience: Dict, content_pillars: List[str]) -> Dict[str, Any]:
        """Create a comprehensive content strategy."""
        prompt = f"""Develop a content strategy based on:

Business Goals: {', '.join(business_goals)}
Target Audience: {target_audience}
Content Pillars: {', '.join(content_pillars)}

Provide:
1. Content mission statement
2. Audience personas and content preferences
3. Content mix by funnel stage
4. Format recommendations (blog, video, social, etc.)
5. Publishing frequency and channels
6. Content governance guidelines
7. Success metrics and KPIs"""
        
        return await self.execute(prompt)
    
    async def generate_content_ideas(self, topic: str, target_audience: str, count: int = 10, content_type: str = "blog_post") -> List[Dict[str, Any]]:
        """Generate content ideas for a specific topic."""
        prompt = f"""Generate {count} content ideas:

Topic: {topic}
Target Audience: {target_audience}
Content Type: {content_type}

For each idea provide:
- Compelling title
- Brief description
- Target keywords
- Funnel stage (awareness, consideration, decision)
- Estimated word count/length
- Suggested CTA"""
        
        return await self.execute(prompt)
    
    async def create_editorial_calendar(self, strategy: Dict, timeframe: str, channels: List[str]) -> Dict[str, Any]:
        """Create an editorial calendar based on strategy."""
        prompt = f"""Create an editorial calendar:

Strategy: {strategy}
Timeframe: {timeframe}
Channels: {', '.join(channels)}

Provide:
1. Weekly content schedule
2. Content topics and titles
3. Publishing dates and times
4. Channel distribution
5. Content formats
6. Responsible team members
7. Key milestones and campaigns"""
        
        return await self.execute(prompt)
    
    async def create_content_brief(self, topic: str, target_keywords: List[str], content_type: str = "blog_post") -> Dict[str, Any]:
        """Create a detailed content brief for writers."""
        prompt = f"""Create a comprehensive content brief:

Topic: {topic}
Target Keywords: {', '.join(target_keywords)}
Content Type: {content_type}

Provide:
1. Content objective and goal
2. Target audience and their needs
3. Suggested outline and structure
4. Key points to cover
5. SEO requirements (keywords, meta, etc.)
6. Internal linking suggestions
7. Visual content recommendations
8. CTA recommendations
9. Word count guidelines
10. Tone and style guidelines"""
        
        return await self.execute(prompt)
    
    async def analyze_content_performance(self, content_data: List[Dict], goals: Dict) -> Dict[str, Any]:
        """Analyze content performance and provide recommendations."""
        prompt = f"""Analyze content performance:

Content Data: {content_data}
Goals: {goals}

Provide:
1. Performance summary (top/bottom performers)
2. Engagement analysis
3. SEO performance review
4. Content gap analysis
5. Optimization recommendations
6. Content refresh suggestions
7. Future content recommendations"""
        
        return await self.execute(prompt)


# Singleton instance
_content_manager_instance = None

def get_content_manager_agent(memory: Optional[AgentMemory] = None, **kwargs) -> ContentManagerAgent:
    """Get or create the Content Manager agent instance."""
    global _content_manager_instance
    if _content_manager_instance is None:
        _content_manager_instance = ContentManagerAgent(memory=memory, **kwargs)
    return _content_manager_instance