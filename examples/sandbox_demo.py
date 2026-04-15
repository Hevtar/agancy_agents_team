#!/usr/bin/env python3
"""
Sandbox demonstration of the Agency system.
This script runs a complete workflow in isolated sandbox mode.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import settings
from core.base_agent import BaseAgent, AgentMemory
from core.event_bus import EventBus, Event, EventType, get_event_bus
from tools.registry import get_tools_registry
from tools.analytics_tools import analyze_data_trends, calculate_conversion_funnel
from tools.marketing_tools import generate_content_ideas, generate_social_media_posts, analyze_seo_potential
from tools.technical_tools import generate_sql_query, validate_data_schema


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_step(step: str, content: str):
    """Print a step with content."""
    print(f"\n[{step}]")
    print(content)


async def demo_basic_tools():
    """Demonstrate basic tool usage."""
    print_section("DEMO 1: Basic Tools Usage")
    
    # 1. Content Ideas Generation
    print_step("1.1", "Generating content ideas...")
    ideas = generate_content_ideas(
        topic="Digital Marketing Trends",
        target_audience="Small business owners",
        content_type="blog_post",
        count=3
    )
    print(f"Generated {len(ideas)} content ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. {idea['title']}")
    
    # 2. SEO Analysis
    print_step("1.2", "Analyzing SEO potential...")
    seo_analysis = analyze_seo_potential(
        keyword="digital marketing trends 2024",
        content_length=1500,
        competition_level="medium"
    )
    print(f"SEO Score: {seo_analysis['seo_score']}/100")
    print(f"Competition: {seo_analysis['competition_level']}")
    print("Top recommendations:")
    for rec in seo_analysis['recommendations'][:3]:
        print(f"  • {rec}")
    
    # 3. Social Media Posts
    print_step("1.3", "Generating social media posts...")
    posts = generate_social_media_posts(
        topic="New product launch",
        platforms=["twitter", "linkedin"],
        tone="professional",
        count=2
    )
    print(f"Generated {len(posts)} social media posts:")
    for post in posts:
        print(f"  [{post['platform']}] {post['content'][:80]}...")
    
    # 4. Campaign Metrics
    print_step("1.4", "Calculating campaign metrics...")
    metrics = calculate_campaign_metrics(
        impressions=100000,
        clicks=2500,
        conversions=125,
        spend=500.0,
        revenue=2500.0
    )
    print("Campaign Performance:")
    print(f"  CTR: {metrics['ctr']}%")
    print(f"  Conversion Rate: {metrics['conversion_rate']}%")
    print(f"  CPC: ${metrics['cpc']}")
    print(f"  ROAS: {metrics['roas']}x")
    print(f"  ROI: {metrics['roi']}%")
    
    # 5. SQL Query Generation
    print_step("1.5", "Generating SQL query...")
    schema = {
        "id": "integer",
        "name": "string",
        "email": "string",
        "created_at": "timestamp",
        "total_spent": "decimal"
    }
    sql_result = generate_sql_query(
        table_schema=schema,
        query_intent="Show me the top 10 customers by total spent",
        database_type="postgresql"
    )
    print(f"Generated SQL Query:")
    print(f"  {sql_result['sql_query']}")


async def demo_event_bus():
    """Demonstrate event bus functionality."""
    print_section("DEMO 2: Event Bus Communication")
    
    # Get event bus
    event_bus = get_event_bus()
    
    # Track received events
    received_events = []
    
    def event_handler(event: Event):
        received_events.append(event)
        print(f"  Received event: {event.type.value} from {event.source}")
    
    # Subscribe to events
    event_bus.subscribe(
        callback=event_handler,
        event_types=[EventType.TASK_STARTED, EventType.TASK_COMPLETED]
    )
    
    print_step("2.1", "Publishing events...")
    
    # Publish some events
    await event_bus.publish(Event(
        type=EventType.TASK_STARTED,
        source="content_manager",
        target="seo_copywriter",
        data={"task": "write_article", "topic": "AI in Marketing"}
    ))
    
    await event_bus.publish(Event(
        type=EventType.TASK_COMPLETED,
        source="seo_copywriter",
        data={"result": "Article completed", "word_count": 1500}
    ))
    
    await event_bus.publish(Event(
        type=EventType.TASK_STARTED,
        source="data_analyst",
        data={"task": "analyze_campaign"}
    ))
    
    # Wait for processing
    await asyncio.sleep(0.5)
    
    print(f"\nTotal events received: {len(received_events)}")
    
    # Show event history
    print_step("2.2", "Event History")
    history = event_bus.get_event_history(limit=10)
    for event in history:
        print(f"  {event.timestamp.strftime('%H:%M:%S')} - {event.type.value} from {event.source}")


async def demo_agent_workflow():
    """Demonstrate a simple agent workflow."""
    print_section("DEMO 3: Simple Agent Workflow")
    
    # Create a simple agent
    print_step("3.1", "Creating Content Manager Agent...")
    
    content_manager = BaseAgent(
        name="content_manager",
        role="Content Marketing Manager",
        goal="Create engaging content strategies and plans",
        system_prompt="""You are an experienced Content Marketing Manager.
Your job is to create content strategies, generate ideas, and plan content calendars.
You always focus on the target audience and SEO best practices.""",
        allow_delegation=False,
        verbose=True
    )
    
    # Create another agent
    print_step("3.2", "Creating SEO Specialist Agent...")
    
    seo_specialist = BaseAgent(
        name="seo_specialist",
        role="SEO Specialist",
        goal="Optimize content for search engines",
        system_prompt="""You are an SEO expert with 10 years of experience.
You analyze content for SEO opportunities and provide actionable recommendations.
You focus on keyword optimization, technical SEO, and content structure.""",
        allow_delegation=False,
        verbose=True
    )
    
    # Simulate workflow
    print_step("3.3", "Running Content Creation Workflow...")
    
    # Task 1: Generate content ideas
    task1_input = {
        "topic": "Sustainable Business Practices",
        "target_audience": "B2B companies",
        "goal": "Generate 5 blog post ideas"
    }
    
    print("  Content Manager working on task 1...")
    # In a real scenario, this would call the LLM
    ideas = generate_content_ideas(
        topic=task1_input["topic"],
        target_audience=task1_input["target_audience"],
        count=5
    )
    print(f"  Generated {len(ideas)} ideas:")
    for idea in ideas[:3]:
        print(f"    • {idea['title']}")
    
    # Task 2: SEO optimization
    task2_input = {
        "content_topic": "Sustainable Business Practices",
        "target_keywords": ["sustainable business", "eco-friendly practices"]
    }
    
    print("\n  SEO Specialist working on task 2...")
    seo_analysis = analyze_seo_potential(
        keyword=task2_input["target_keywords"][0],
        content_length=2000
    )
    print(f"  SEO Score: {seo_analysis['seo_score']}/100")
    print("  Recommendations:")
    for rec in seo_analysis['recommendations'][:3]:
        print(f"    • {rec}")
    
    print("\n  ✓ Workflow completed successfully!")


async def demo_data_validation():
    """Demonstrate data validation tool."""
    print_section("DEMO 4: Data Validation")
    
    print_step("4.1", "Validating data against schema...")
    
    # Define schema
    user_schema = {
        "name": {"type": "string", "required": True, "min_length": 2, "max_length": 100},
        "email": {"type": "string", "required": True, "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"},
        "age": {"type": "integer", "required": False, "min": 18, "max": 120},
        "is_subscriber": {"type": "boolean", "required": False}
    }
    
    # Valid data
    valid_user = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "is_subscriber": True
    }
    
    result = validate_data_schema(valid_user, user_schema)
    print(f"  Valid data test: {'PASS' if result['is_valid'] else 'FAIL'}")
    
    # Invalid data
    invalid_user = {
        "name": "J",  # Too short
        "email": "invalid-email",  # Invalid format
        "age": 150,  # Above max
        "extra_field": "not in schema"
    }
    
    result = validate_data_schema(invalid_user, user_schema)
    print(f"  Invalid data test: {'PASS' if not result['is_valid'] else 'FAIL'}")
    print(f"  Errors found: {result['error_count']}")
    for error in result['errors']:
        print(f"    • {error}")
    print(f"  Warnings: {result['warning_count']}")
    for warning in result['warnings']:
        print(f"    • {warning}")


async def demo_tools_registry():
    """Demonstrate tools registry functionality."""
    print_section("DEMO 5: Tools Registry")
    
    registry = get_tools_registry()
    
    print_step("5.1", "Listing available tools...")
    all_tools = registry.list_tools()
    print(f"  Total tools registered: {len(all_tools)}")
    
    categories = registry.list_categories()
    print(f"  Categories: {', '.join(categories)}")
    
    print_step("5.2", "Tools by category...")
    for category in categories:
        tools = registry.get_tools_by_category(category)
        print(f"  {category}: {len(tools)} tools")
        for tool in tools[:3]:
            print(f"    • {tool.name}")
        if len(tools) > 3:
            print(f"    ... and {len(tools) - 3} more")
    
    print_step("5.3", "Tool schema example...")
    schema = registry.get_tool_schema("analyze_seo_potential")
    print(f"  Tool: {schema['name']}")
    print(f"  Description: {schema['description']}")
    print("  Parameters:")
    for param_name, param_info in schema['parameters']['properties'].items():
        print(f"    • {param_name}: {param_info['type']}")


async def main():
    """Run all demos."""
    print("=" * 60)
    print("  AGENCY SYSTEM - SANDBOX DEMO")
    print("  Testing core functionality in isolated mode")
    print("=" * 60)
    
    try:
        # Run demos
        await demo_basic_tools()
        await demo_event_bus()
        await demo_agent_workflow()
        await demo_data_validation()
        await demo_tools_registry()
        
        print_section("DEMO COMPLETED")
        print("  ✓ All demonstrations completed successfully!")
        print("  ✓ System is ready for production use")
        print("\n  Next steps:")
        print("    1. Configure .env with your API keys")
        print("    2. Start Docker services: cd infra && docker-compose up -d")
        print("    3. Initialize database: python scripts/init_db.py")
        print("    4. Start the API server: python api/main.py")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)