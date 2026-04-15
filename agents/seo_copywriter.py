"""
SEO Copywriter Agent - Writes SEO-optimized content.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class SEOCopywriterAgent(BaseAgent):
    """
    SEO Copywriter Agent responsible for:
    - Writing SEO-optimized articles and content
    - Keyword research and implementation
    - Content optimization for search engines
    - Meta descriptions and title optimization
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an expert SEO Copywriter with 8+ years of experience creating content that ranks.
Your role is to write compelling, SEO-optimized content that satisfies both search engines and readers.

Key responsibilities:
1. Write SEO-optimized articles and web content
2. Implement keyword research findings
3. Optimize content structure and readability
4. Create compelling meta titles and descriptions
5. Ensure content satisfies search intent
6. Balance SEO requirements with user experience

You are a skilled writer who understands SEO best practices.
You create content that ranks well while providing genuine value to readers.

When writing content:
- Research and understand search intent
- Use keywords naturally and strategically
- Create comprehensive, authoritative content
- Optimize headings and structure
- Include internal and external links
- Write compelling meta descriptions
- Ensure readability and engagement
- Follow on-page SEO best practices

You excel at creating content that both ranks and converts."""
        
        super().__init__(
            name="seo_copywriter",
            role="SEO Copywriter",
            goal="Create SEO-optimized content that ranks well and engages readers",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def write_article(self, topic: str, target_keywords: List[str], outline: Dict, word_count: int = 1500) -> Dict[str, Any]:
        """Write an SEO-optimized article."""
        prompt = f"""Write an SEO-optimized article:

Topic: {topic}
Target Keywords: {', '.join(target_keywords)}
Outline: {outline}
Word Count: {word_count}

Provide:
1. SEO-optimized title (under 60 characters)
2. Meta description (under 160 characters)
3. Full article content with proper heading structure (H1, H2, H3)
4. Natural keyword placement throughout
5. Internal linking suggestions
6. Image alt text recommendations
7. FAQ section if appropriate
8. Call-to-action

Ensure the content is comprehensive, engaging, and optimized for search intent."""
        
        return await self.execute(prompt)
    
    async def optimize_existing_content(self, content: str, target_keywords: List[str], current_performance: Optional[Dict] = None) -> Dict[str, Any]:
        """Optimize existing content for better SEO performance."""
        prompt = f"""Optimize this content for SEO:

Content: {content[:1000]}... (truncated)
Target Keywords: {', '.join(target_keywords)}
Current Performance: {current_performance or 'No data available'}

Provide:
1. SEO analysis of current content
2. Keyword optimization recommendations
3. Content structure improvements
4. Meta tag optimization suggestions
5. Internal linking opportunities
6. Content expansion suggestions
7. Readability improvements
8. Expected impact of optimizations"""
        
        return await self.execute(prompt)
    
    async def create_meta_descriptions(self, page_content: str, target_keywords: List[str], count: int = 3) -> List[Dict[str, Any]]:
        """Create multiple meta description options."""
        prompt = f"""Create {count} meta description options:

Page Content: {page_content[:500]}... (truncated)
Target Keywords: {', '.join(target_keywords)}

For each option provide:
- Meta title (under 60 characters)
- Meta description (under 160 characters)
- Focus keyword
- Unique value proposition
- Call-to-action element

Ensure each option is compelling and click-worthy."""
        
        return await self.execute(prompt)
    
    async def write_product_descriptions(self, product_name: str, features: List[str], target_audience: str, tone: str = "professional") -> Dict[str, Any]:
        """Write SEO-optimized product descriptions."""
        prompt = f"""Write SEO-optimized product descriptions:

Product: {product_name}
Features: {', '.join(features)}
Target Audience: {target_audience}
Tone: {tone}

Provide:
1. Short description (1-2 sentences)
2. Medium description (paragraph)
3. Long description (detailed)
4. Bullet point features/benefits
5. Meta title and description
6. Target keywords
7. Unique selling propositions"""
        
        return await self.execute(prompt)


# Singleton instance
_seo_copywriter_instance = None

def get_seo_copywriter_agent(memory: Optional[AgentMemory] = None, **kwargs) -> SEOCopywriterAgent:
    """Get or create the SEO Copywriter agent instance."""
    global _seo_copywriter_instance
    if _seo_copywriter_instance is None:
        _seo_copywriter_instance = SEOCopywriterAgent(memory=memory, **kwargs)
    return _seo_copywriter_instance