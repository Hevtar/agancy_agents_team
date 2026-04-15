"""
SEO Specialist Agent - Technical SEO and optimization expert.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class SEOSpecialistAgent(BaseAgent):
    """
    SEO Specialist Agent responsible for:
    - Technical SEO audits and optimization
    - Keyword research and strategy
    - On-page SEO optimization
    - Link building strategy
    - SEO performance monitoring
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an SEO Specialist with deep technical expertise and 8+ years of experience.
Your role is to ensure websites are optimized for search engines and provide excellent user experience.

Key responsibilities:
1. Conduct technical SEO audits
2. Develop keyword strategies
3. Optimize on-page elements
4. Build link acquisition strategies
5. Monitor SEO performance and rankings
6. Stay updated with algorithm changes

You are technical, analytical, and detail-oriented.
You understand both the technical and content aspects of SEO.

When performing SEO analysis:
- Start with comprehensive technical audit
- Analyze site architecture and crawlability
- Review content quality and relevance
- Assess backlink profile
- Monitor rankings and traffic patterns
- Provide actionable, prioritized recommendations
- Consider user experience alongside SEO
- Follow white-hat SEO practices

You excel at improving organic visibility and driving qualified traffic."""
        
        super().__init__(
            name="seo_specialist",
            role="SEO Specialist",
            goal="Optimize websites for search engines and improve organic visibility",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def conduct_technical_audit(self, website_url: str, audit_depth: str = "comprehensive") -> Dict[str, Any]:
        """Conduct a comprehensive technical SEO audit."""
        prompt = f"""Conduct a technical SEO audit:

Website: {website_url}
Audit Depth: {audit_depth}

Provide:
1. Crawlability analysis (robots.txt, sitemaps)
2. Site architecture review
3. Page speed analysis
4. Mobile-friendliness assessment
5. Schema markup review
6. Internal linking analysis
7. URL structure evaluation
8. Canonicalization issues
9. Duplicate content analysis
10. Indexation status review
11. Core Web Vitals assessment
12. Prioritized action items"""
        
        return await self.execute(prompt)
    
    async def perform_keyword_research(self, seed_keywords: List[str], target_audience: str, competition_level: str = "medium") -> Dict[str, Any]:
        """Perform comprehensive keyword research."""
        prompt = f"""Perform keyword research:

Seed Keywords: {', '.join(seed_keywords)}
Target Audience: {target_audience}
Competition Level: {competition_level}

Provide:
1. Keyword list with search volumes
2. Keyword difficulty analysis
3. Search intent classification
4. Long-tail keyword opportunities
5. Competitor keyword analysis
6. Keyword grouping recommendations
7. Content gap analysis
8. Priority keyword recommendations
9. Seasonal trends analysis
10. SERP feature opportunities"""
        
        return await self.execute(prompt)
    
    async def optimize_on_page(self, page_content: str, target_keywords: List[str], current_rankings: Optional[Dict] = None) -> Dict[str, Any]:
        """Optimize on-page SEO elements."""
        prompt = f"""Optimize on-page SEO:

Page Content: {page_content[:1000]}... (truncated)
Target Keywords: {', '.join(target_keywords)}
Current Rankings: {current_rankings or 'New page'}

Provide:
1. Title tag optimization
2. Meta description optimization
3. Heading structure optimization
4. Content optimization recommendations
5. Keyword placement suggestions
6. Internal linking opportunities
7. Image optimization (alt text, file names)
8. URL structure recommendations
9. Schema markup suggestions
10. Content length recommendations
11. Readability improvements"""
        
        return await self.execute(prompt)
    
    async def develop_link_building_strategy(self, industry: str, target_keywords: List[str], current_backlinks: Optional[Dict] = None) -> Dict[str, Any]:
        """Develop a comprehensive link building strategy."""
        prompt = f"""Develop a link building strategy:

Industry: {industry}
Target Keywords: {', '.join(target_keywords)}
Current Backlinks: {current_backlinks or 'New domain'}

Provide:
1. Backlink profile analysis
2. Competitor backlink analysis
3. Link building opportunities
4. Content-based link attraction strategies
5. Guest posting recommendations
6. Digital PR opportunities
7. Resource page targets
8. Broken link building opportunities
9. Link velocity recommendations
10. Risk assessment and mitigation
11. Success metrics and tracking"""
        
        return await self.execute(prompt)
    
    async def analyze_seo_performance(self, performance_data: Dict, goals: Dict, timeframe: str) -> Dict[str, Any]:
        """Analyze SEO performance and provide recommendations."""
        prompt = f"""Analyze SEO performance:

Performance Data: {performance_data}
Goals: {goals}
Timeframe: {timeframe}

Provide:
1. Rankings analysis and trends
2. Organic traffic analysis
3. Click-through rate analysis
4. Conversion rate from organic
5. Keyword performance review
6. Technical issues impact
7. Competitor comparison
8. Algorithm update impact
9. ROI analysis
10. Prioritized recommendations
11. Next period forecasting"""
        
        return await self.execute(prompt)


# Singleton instance
_seo_specialist_instance = None

def get_seo_specialist_agent(memory: Optional[AgentMemory] = None, **kwargs) -> SEOSpecialistAgent:
    """Get or create the SEO Specialist agent instance."""
    global _seo_specialist_instance
    if _seo_specialist_instance is None:
        _seo_specialist_instance = SEOSpecialistAgent(memory=memory, **kwargs)
    return _seo_specialist_instance