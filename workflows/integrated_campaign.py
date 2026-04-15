"""
Integrated Campaign Workflow - Multi-channel marketing campaign orchestration.
"""
from typing import Dict, List, Optional, Any
from workflows.base_workflow import BaseWorkflow


class IntegratedCampaignWorkflow(BaseWorkflow):
    """
    Integrated Campaign Workflow that orchestrates multiple agents
    to create and execute a comprehensive multi-channel marketing campaign.
    
    This workflow demonstrates the collaboration between:
    - Marketing Strategist: Overall campaign strategy
    - Content Manager: Content planning and coordination
    - SEO Copywriter: SEO-optimized content creation
    - Social Media Manager: Social media content and scheduling
    - Email Marketing Manager: Email campaign creation
    - PPC Specialist: Paid advertising setup
    - Data Analyst: Performance tracking and analysis
    """
    
    def __init__(self):
        super().__init__(
            name="integrated_campaign",
            description="Multi-channel marketing campaign orchestration workflow"
        )
    
    def setup_workflow(self, agents: Dict[str, Any]) -> "IntegratedCampaignWorkflow":
        """
        Setup the integrated campaign workflow with agents.
        
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
            name="campaign_strategy",
            agent_name="marketing_strategist",
            method="create_campaign_strategy",
            inputs={
                "business_goals": "{{business_goals}}",
                "target_audience": "{{target_audience}}",
                "budget": "{{budget}}",
                "timeline": "{{timeline}}",
                "channels": "{{channels}}"
            }
        )
        
        self.add_step(
            name="content_plan",
            agent_name="content_manager",
            method="create_content_plan",
            inputs={
                "campaign_strategy": "{{campaign_strategy}}",
                "content_types": "{{content_types}}",
                "frequency": "{{frequency}}"
            }
        )
        
        self.add_step(
            name="seo_content",
            agent_name="seo_copywriter",
            method="create_seo_content_plan",
            inputs={
                "content_plan": "{{content_plan}}",
                "target_keywords": "{{keywords}}",
                "content_pillars": "{{content_pillars}}"
            }
        )
        
        self.add_step(
            name="social_media_plan",
            agent_name="social_media_manager",
            method="create_social_media_plan",
            inputs={
                "campaign_strategy": "{{campaign_strategy}}",
                "content_plan": "{{content_plan}}",
                "platforms": "{{social_platforms}}"
            }
        )
        
        self.add_step(
            name="email_campaigns",
            agent_name="email_marketing_manager",
            method="create_email_strategy",
            inputs={
                "business_goals": "{{business_goals}}",
                "target_audience": "{{target_audience}}",
                "email_frequency": "{{email_frequency}}"
            }
        )
        
        self.add_step(
            name="ppc_campaigns",
            agent_name="ppc_specialist",
            method="create_ppc_campaign",
            inputs={
                "campaign_goal": "{{campaign_goal}}",
                "target_keywords": "{{keywords}}",
                "budget": "{{ppc_budget}}",
                "platforms": "{{ppc_platforms}}"
            }
        )
        
        self.add_step(
            name="analytics_setup",
            agent_name="data_analyst",
            method="setup_tracking",
            inputs={
                "campaign_strategy": "{{campaign_strategy}}",
                "channels": "{{channels}}",
                "kpis": "{{kpis}}"
            }
        )
        
        return self
    
    async def execute_campaign(self, campaign_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the integrated campaign workflow.
        
        Args:
            campaign_params: Campaign parameters including goals, audience, budget, etc.
            
        Returns:
            Campaign execution results
        """
        return await self.execute(campaign_params)
    
    def get_campaign_template(self) -> Dict[str, Any]:
        """
        Get a template for campaign parameters.
        
        Returns:
            Campaign parameter template
        """
        return {
            "business_goals": ["Increase brand awareness", "Generate leads", "Drive sales"],
            "target_audience": {
                "demographics": "25-45 years old",
                "interests": ["technology", "marketing", "business"],
                "behavior": "Active online shoppers"
            },
            "budget": 10000,
            "timeline": "3 months",
            "channels": ["social_media", "email", "search", "display"],
            "content_types": ["blog_posts", "social_posts", "emails", "ads"],
            "frequency": "daily",
            "keywords": ["marketing automation", "digital marketing", "campaign management"],
            "content_pillars": ["Education", "Product", "Industry Trends"],
            "social_platforms": ["facebook", "instagram", "linkedin", "twitter"],
            "email_frequency": "weekly",
            "campaign_goal": "Lead generation",
            "ppc_budget": 3000,
            "ppc_platforms": ["google_ads", "facebook_ads"],
            "kpis": ["impressions", "clicks", "conversions", "ROAS"]
        }