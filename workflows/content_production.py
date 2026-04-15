"""
Content Production Workflow - Streamlined content creation pipeline.
"""
from typing import Dict, List, Optional, Any
from workflows.base_workflow import BaseWorkflow


class ContentProductionWorkflow(BaseWorkflow):
    """
    Content Production Workflow that orchestrates the content creation process
    from ideation to publication.
    
    This workflow demonstrates collaboration between:
    - Content Manager: Content planning and coordination
    - SEO Copywriter: SEO-optimized content creation
    - SEO Specialist: SEO review and optimization
    - Brand Manager: Brand consistency review
    - UX Designer: Content UX review
    """
    
    def __init__(self):
        super().__init__(
            name="content_production",
            description="Streamlined content creation pipeline workflow"
        )
    
    def setup_workflow(self, agents: Dict[str, Any]) -> "ContentProductionWorkflow":
        """
        Setup the content production workflow with agents.
        
        Args:
            agents: Dictionary of agent instances
            
        Returns:
            Configured workflow instance
        """
        # Add agents
        for name, agent in agents.items():
            self.add_agent(name, agent)
        
        # Define workflow steps
        self.add_step(
            name="content_brief",
            agent_name="content_manager",
            method="create_content_brief",
            inputs={
                "content_type": "{{content_type}}",
                "topic": "{{topic}}",
                "target_audience": "{{target_audience}}",
                "goals": "{{goals}}"
            }
        )
        
        self.add_step(
            name="keyword_research",
            agent_name="seo_specialist",
            method="research_keywords",
            inputs={
                "topic": "{{topic}}",
                "content_type": "{{content_type}}",
                "competitors": "{{competitors}}"
            }
        )
        
        self.add_step(
            name="content_creation",
            agent_name="seo_copywriter",
            method="write_content",
            inputs={
                "content_brief": "{{content_brief}}",
                "keywords": "{{keyword_research}}",
                "tone": "{{tone}}",
                "length": "{{length}}"
            }
        )
        
        self.add_step(
            name="seo_review",
            agent_name="seo_specialist",
            method="review_seo",
            inputs={
                "content": "{{content_creation}}",
                "keywords": "{{keyword_research}}",
                "target_score": "{{target_seo_score}}"
            }
        )
        
        self.add_step(
            name="brand_review",
            agent_name="brand_manager",
            method="review_brand_consistency",
            inputs={
                "content": "{{content_creation}}",
                "brand_guidelines": "{{brand_guidelines}}"
            }
        )
        
        self.add_step(
            name="ux_review",
            agent_name="ux_designer",
            method="review_content_ux",
            inputs={
                "content": "{{content_creation}}",
                "format": "{{content_type}}",
                "platform": "{{platform}}"
            }
        )
        
        self.add_step(
            name="final_optimization",
            agent_name="content_manager",
            method="finalize_content",
            inputs={
                "content": "{{content_creation}}",
                "seo_feedback": "{{seo_review}}",
                "brand_feedback": "{{brand_review}}",
                "ux_feedback": "{{ux_review}}"
            }
        )
        
        return self
    
    async def produce_content(self, content_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the content production workflow.
        
        Args:
            content_params: Content parameters including topic, type, audience, etc.
            
        Returns:
            Content production results
        """
        return await self.execute(content_params)
    
    def get_content_template(self) -> Dict[str, Any]:
        """
        Get a template for content parameters.
        
        Returns:
            Content parameter template
        """
        return {
            "content_type": "blog_post",
            "topic": "Digital Marketing Trends 2024",
            "target_audience": "Marketing professionals and business owners",
            "goals": ["Educate", "Generate leads", "Establish thought leadership"],
            "competitors": ["competitor1.com", "competitor2.com"],
            "tone": "professional yet approachable",
            "length": "1500-2000 words",
            "target_seo_score": 85,
            "brand_guidelines": {
                "voice": "Professional, friendly, authoritative",
                "style": "Clear, concise, data-driven",
                "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
                "typography": "Modern sans-serif"
            },
            "platform": "website"
        }