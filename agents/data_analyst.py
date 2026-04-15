"""
Data Analyst Agent - Analyzes marketing data and provides insights.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory


class DataAnalystAgent(BaseAgent):
    """
    Data Analyst Agent responsible for:
    - Analyzing marketing performance data
    - Creating data visualizations and reports
    - Identifying trends and patterns
    - Providing actionable insights
    - Statistical analysis and forecasting
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are a Senior Data Analyst with expertise in marketing analytics.
Your role is to transform raw marketing data into actionable insights that drive business decisions.

Key responsibilities:
1. Analyze marketing performance across channels
2. Create comprehensive reports and dashboards
3. Identify trends, patterns, and anomalies
4. Provide data-driven recommendations
5. Build predictive models and forecasts
6. Statistical analysis and hypothesis testing

You are analytical, detail-oriented, and skilled at data storytelling.
You excel at finding meaningful insights in complex datasets.

When analyzing data:
- Start with clear business questions
- Ensure data quality and validity
- Use appropriate statistical methods
- Visualize data effectively
- Provide context and benchmarks
- Highlight actionable insights
- Explain technical concepts clearly
- Make data-driven recommendations

You turn data into strategic advantage."""
        
        super().__init__(
            name="data_analyst",
            role="Data Analyst",
            goal="Transform marketing data into actionable insights and recommendations",
            system_prompt=system_prompt,
            allow_delegation=False,
            memory=memory,
            **kwargs
        )
    
    async def analyze_campaign_performance(self, campaign_data: Dict, benchmarks: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze marketing campaign performance."""
        prompt = f"""Analyze this marketing campaign performance:

Campaign Data: {campaign_data}
Benchmarks: {benchmarks or 'Industry averages'}

Provide:
1. Performance summary (KPIs vs goals)
2. Channel-by-channel analysis
3. Conversion funnel analysis
4. ROI and ROAS calculation
5. Statistical significance testing
6. Trend analysis
7. Anomaly detection
8. Actionable recommendations
9. Optimization opportunities"""
        
        return await self.execute(prompt)
    
    async def identify_trends(self, historical_data: List[Dict], timeframe: str, metrics: List[str]) -> Dict[str, Any]:
        """Identify trends in historical marketing data."""
        prompt = f"""Identify trends in this marketing data:

Historical Data: {historical_data}
Timeframe: {timeframe}
Metrics to Analyze: {', '.join(metrics)}

Provide:
1. Trend analysis for each metric
2. Seasonal patterns identification
3. Growth rate calculations
4. Correlation analysis
5. Anomaly detection
6. Statistical significance
7. Predictive insights
8. Recommendations based on trends"""
        
        return await self.execute(prompt)
    
    async def create_segmentation_analysis(self, customer_data: List[Dict], segmentation_criteria: List[str]) -> Dict[str, Any]:
        """Perform customer segmentation analysis."""
        prompt = f"""Perform customer segmentation analysis:

Customer Data: {customer_data}
Segmentation Criteria: {', '.join(segmentation_criteria)}

Provide:
1. Segmentation methodology
2. Identified customer segments
3. Segment profiles and characteristics
4. Segment size and value analysis
5. Behavioral patterns by segment
6. Recommendations for each segment
7. Targeting and personalization strategies"""
        
        return await self.execute(prompt)
    
    async def build_forecast_model(self, historical_data: List[Dict], forecast_period: str, target_metric: str) -> Dict[str, Any]:
        """Build a forecasting model for marketing metrics."""
        prompt = f"""Build a forecasting model:

Historical Data: {historical_data}
Forecast Period: {forecast_period}
Target Metric: {target_metric}

Provide:
1. Forecasting methodology
2. Model selection rationale
3. Key drivers and variables
4. Forecast results with confidence intervals
5. Assumptions and limitations
6. Scenario analysis (best/worst case)
7. Monitoring and validation approach"""
        
        return await self.execute(prompt)
    
    async def perform_attribution_analysis(self, conversion_data: List[Dict], attribution_models: List[str]) -> Dict[str, Any]:
        """Perform multi-touch attribution analysis."""
        prompt = f"""Perform attribution analysis:

Conversion Data: {conversion_data}
Attribution Models: {', '.join(attribution_models)}

Provide:
1. Attribution model comparison
2. Channel contribution analysis
3. Touchpoint effectiveness
4. Customer journey insights
5. Budget allocation recommendations
6. Cross-channel synergies
7. Optimization opportunities"""
        
        return await self.execute(prompt)


# Singleton instance
_data_analyst_instance = None

def get_data_analyst_agent(memory: Optional[AgentMemory] = None, **kwargs) -> DataAnalystAgent:
    """Get or create the Data Analyst agent instance."""
    global _data_analyst_instance
    if _data_analyst_instance is None:
        _data_analyst_instance = DataAnalystAgent(memory=memory, **kwargs)
    return _data_analyst_instance