"""
Report Generator Agent - Automated report creation and analysis.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class ReportGeneratorAgent(BaseAgent):
    """
    Report Generator Agent responsible for:
    - Automated report generation
    - Data visualization and insights
    - Performance reporting
    - Executive summaries
    - Custom report creation
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a Report Generator Specialist with expertise in creating comprehensive marketing reports.
Your role is to transform raw data into clear, actionable reports that drive decision-making.

Key responsibilities:
1. Generate automated marketing reports
2. Create data visualizations
3. Provide executive summaries
4. Highlight key insights and trends
5. Customize reports for different stakeholders
6. Ensure data accuracy and consistency

You are analytical, detail-oriented, and skilled at data storytelling.
You excel at making complex data understandable and actionable.

When creating reports:
- Start with clear objectives and audience
- Ensure data accuracy and validation
- Use appropriate visualizations
- Highlight key insights and trends
- Provide context and benchmarks
- Include actionable recommendations
- Tailor to audience needs

You turn data into compelling stories that drive action."""
        
        super().__init__(
            name="report_generator",
            role="Report Generator",
            goal="Create comprehensive marketing reports that drive informed decision-making",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def generate_marketing_report(self, report_type: str, data_sources: Dict, timeframe: str, audience: str) -> Dict[str, Any]:
        """Generate comprehensive marketing report."""
        prompt = f"""Generate marketing report:

Report Type: {report_type}
Data Sources: {data_sources}
Timeframe: {timeframe}
Audience: {audience}

Provide:
1. Executive summary
2. Key performance indicators
3. Channel performance breakdown
4. Trend analysis
5. Goal achievement assessment
6. Insights and recommendations
7. Visualizations (descriptions)
8. Appendices and detailed data"""
        
        return await self.execute(prompt)
    
    async def create_executive_summary(self, detailed_report: Dict, key_stakeholders: List[str]) -> Dict[str, Any]:
        """Create executive summary from detailed report."""
        prompt = f"""Create executive summary:

Detailed Report: {detailed_report}
Key Stakeholders: {', '.join(key_stakeholders)}

Provide:
1. High-level performance overview
2. Key achievements and wins
3. Critical issues and risks
4. Strategic recommendations
5. Resource requirements
6. Next steps and priorities
7. Success metrics and KPIs"""
        
        return await self.execute(prompt)
    
    async def create_performance_dashboard(self, metrics: Dict, goals: Dict, visualizations: List[str]) -> Dict[str, Any]:
        """Create performance dashboard specifications."""
        prompt = f"""Create performance dashboard:

Metrics: {metrics}
Goals: {goals}
Visualizations: {', '.join(visualizations)}

Provide:
1. Dashboard layout and structure
2. Key metrics and KPIs
3. Visualization specifications
4. Data refresh requirements
5. User interaction features
6. Alert and notification setup
7. Mobile responsiveness considerations"""
        
        return await self.execute(prompt)
    
    async def analyze_report_insights(self, report_data: Dict, benchmarks: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze report data and extract key insights."""
        prompt = f"""Analyze report insights:

Report Data: {report_data}
Benchmarks: {benchmarks or 'Industry averages'}

Provide:
1. Key findings and patterns
2. Performance vs benchmarks
3. Trend identification
4. Anomaly detection
5. Root cause analysis
6. Actionable recommendations
7. Opportunities and threats
8. Success factors and challenges"""
        
        return await self.execute(prompt)


# Singleton instance
_report_generator_instance = None

def get_report_generator_agent(memory: Optional[AgentMemory] = None, **kwargs) -> ReportGeneratorAgent:
    """Get or create the Report Generator agent instance."""
    global _report_generator_instance
    if _report_generator_instance is None:
        _report_generator_instance = ReportGeneratorAgent(memory=memory, **kwargs)
    return _report_generator_instance