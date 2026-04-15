"""
Marketing and content creation tools.
"""
from typing import Dict, List, Any, Optional
import re
import random
from datetime import datetime, timedelta

from tools.registry import tool


@tool(category="content")
def generate_content_ideas(
    topic: str,
    target_audience: str,
    content_type: str = "blog_post",
    count: int = 5
) -> List[Dict[str, str]]:
    """Generate content ideas for a given topic.
    
    Args:
        topic: Main topic or theme
        target_audience: Description of target audience
        content_type: Type of content (blog_post, social_media, video, email)
        count: Number of ideas to generate
    
    Returns:
        List of content ideas with titles and descriptions
    """
    # Content angle templates based on type
    angles = {
        "blog_post": [
            "How to {topic}: A Complete Guide",
            "Top 10 {topic} Strategies for {audience}",
            "The Ultimate {topic} Toolkit",
            "{topic} Trends in 2024",
            "Common {topic} Mistakes and How to Avoid Them"
        ],
        "social_media": [
            "Quick tip: {topic} hack",
            "Behind the scenes: {topic} process",
            "User-generated content about {topic}",
            "Poll: What's your favorite {topic}?",
            "Share your {topic} story"
        ],
        "video": [
            "Tutorial: {topic} step by step",
            "Interview: Expert talks about {topic}",
            "Case study: {topic} success story",
            "Live Q&A: Ask us about {topic}",
            "Comparison: {topic} tools reviewed"
        ],
        "email": [
            "Your weekly {topic} digest",
            "Exclusive: {topic} tips for subscribers",
            "New resource: {topic} guide",
            "Invitation: {topic} webinar",
            "Survey: Help us improve {topic}"
        ]
    }
    
    ideas = []
    templates = angles.get(content_type, angles["blog_post"])
    
    for i in range(count):
        template = templates[i % len(templates)]
        title = template.format(topic=topic, audience=target_audience)
        
        ideas.append({
            "title": title,
            "description": f"Create {content_type} content about {topic} focusing on {title}",
            "target_audience": target_audience,
            "content_type": content_type,
            "estimated_engagement": random.choice(["high", "medium", "low"])
        })
    
    return ideas


@tool(category="seo")
def analyze_seo_potential(
    keyword: str,
    content_length: int = 1000,
    competition_level: str = "medium"
) -> Dict[str, Any]:
    """Analyze SEO potential for a keyword.
    
    Args:
        keyword: Target keyword
        content_length: Planned content length in words
        competition_level: Competition level (low, medium, high)
    
    Returns:
        SEO analysis with recommendations
    """
    # Simulated SEO metrics
    search_volume = random.randint(100, 10000)
    difficulty = {"low": random.randint(10, 30), 
                  "medium": random.randint(30, 60), 
                  "high": random.randint(60, 90)}[competition_level]
    
    # Recommendations based on analysis
    recommendations = []
    
    if content_length < 1500:
        recommendations.append("Consider increasing content length to 1500+ words for better rankings")
    
    if difficulty > 70:
        recommendations.append("High competition - consider long-tail keyword variations")
    elif difficulty < 30:
        recommendations.append("Low competition - good opportunity for quick wins")
    
    recommendations.extend([
        f"Include keyword in title tag and H1 heading",
        f"Use keyword naturally 2-3 times per 1000 words",
        f"Add related LSI keywords: {keyword} tips, {keyword} guide, best {keyword}",
        f"Optimize meta description (150-160 characters)",
        f"Include internal links to related content"
    ])
    
    return {
        "keyword": keyword,
        "estimated_search_volume": search_volume,
        "competition_difficulty": difficulty,
        "competition_level": competition_level,
        "content_length": content_length,
        "seo_score": max(0, 100 - difficulty + (content_length // 100)),
        "recommendations": recommendations,
        "estimated_ranking_potential": "high" if difficulty < 40 else "medium" if difficulty < 70 else "low"
    }


@tool(category="social_media")
def generate_social_media_posts(
    topic: str,
    platforms: List[str] = None,
    tone: str = "professional",
    count: int = 3
) -> List[Dict[str, str]]:
    """Generate social media posts for different platforms.
    
    Args:
        topic: Main topic or theme
        platforms: List of platforms (twitter, linkedin, instagram, facebook)
        tone: Tone of voice (professional, casual, humorous, inspirational)
        count: Number of posts per platform
    
    Returns:
        List of social media posts optimized for each platform
    """
    if platforms is None:
        platforms = ["twitter", "linkedin", "instagram"]
    
    # Platform-specific constraints
    platform_limits = {
        "twitter": 280,
        "linkedin": 3000,
        "instagram": 2200,
        "facebook": 63206
    }
    
    # Tone modifiers
    tone_modifiers = {
        "professional": "Focus on business value and insights",
        "casual": "Use conversational language and emojis",
        "humorous": "Add wit and playful elements",
        "inspirational": "Focus on motivation and aspirations"
    }
    
    posts = []
    
    for platform in platforms:
        for i in range(count):
            # Generate platform-specific content
            if platform == "twitter":
                content = f"🚀 Quick insight about {topic}: [Key point in under 280 chars]"
            elif platform == "linkedin":
                content = f"Professional perspective on {topic}:\n\n" \
                         f"📊 Industry insight: [Detailed analysis]\n\n" \
                         f"💡 Key takeaway: [Actionable advice]\n\n" \
                         f"#ProfessionalDevelopment #Industry"
            elif platform == "instagram":
                content = f"✨ Visual story about {topic}\n\n" \
                         f"📸 [Describe compelling visual]\n\n" \
                         f"👆 What's your experience with {topic}?\n\n" \
                         f"#{topic.replace(' ', '')} #Content"
            else:  # facebook
                content = f"📝 Discussion about {topic}:\n\n" \
                         f"[Engaging story or question]\n\n" \
                         f"💬 Share your thoughts in the comments!"
            
            posts.append({
                "platform": platform,
                "content": content[:platform_limits.get(platform, 280)],
                "tone": tone,
                "estimated_reach": random.choice(["high", "medium", "low"]),
                "hashtags": [f"#{topic.replace(' ', '')}", f"#{platform}"],
                "optimal_posting_time": f"{random.randint(8, 20)}:{random.choice(['00', '15', '30', '45'])}"
            })
    
    return posts


@tool(category="marketing")
def calculate_campaign_metrics(
    impressions: int,
    clicks: int,
    conversions: int,
    spend: float,
    revenue: float = None
) -> Dict[str, Any]:
    """Calculate key marketing campaign metrics.
    
    Args:
        impressions: Total ad impressions
        clicks: Total clicks received
        conversions: Total conversions
        spend: Total campaign spend
        revenue: Total revenue generated (optional)
    
    Returns:
        Dictionary with calculated metrics
    """
    ctr = (clicks / impressions * 100) if impressions > 0 else 0
    conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
    cpc = (spend / clicks) if clicks > 0 else 0
    cpv = (spend / impressions * 1000) if impressions > 0 else 0
    
    metrics = {
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "spend": spend,
        "ctr": round(ctr, 2),
        "conversion_rate": round(conversion_rate, 2),
        "cpc": round(cpc, 2),
        "cpm": round(cpv, 2)
    }
    
    if revenue is not None:
        roas = (revenue / spend) if spend > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        metrics["revenue"] = revenue
        metrics["roas"] = round(roas, 2)
        metrics["roi"] = round(roi, 2)
    
    # Performance assessment
    performance = "good"
    if ctr < 1 or conversion_rate < 2:
        performance = "needs_improvement"
    elif ctr > 5 and conversion_rate > 5:
        performance = "excellent"
    
    metrics["performance_assessment"] = performance
    
    return metrics


@tool(category="content")
def optimize_content_readability(
    text: str,
    target_grade: int = 8,
    audience: str = "general"
) -> Dict[str, Any]:
    """Analyze and optimize content readability.
    
    Args:
        text: Content text to analyze
        target_grade: Target reading grade level
        audience: Target audience (general, technical, academic, children)
    
    Returns:
        Readability analysis and optimization suggestions
    """
    # Basic text analysis
    sentences = text.split('.')
    words = text.split()
    syllables = sum(1 for char in text.lower() if char in 'aeiou')
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    avg_syllables_per_word = syllables / len(words) if words else 0
    
    # Flesch Reading Ease (simplified)
    flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    flesch_score = max(0, min(100, flesch_score))
    
    # Grade level estimation
    grade_level = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
    
    suggestions = []
    
    if avg_sentence_length > 20:
        suggestions.append("Break down long sentences (current avg: {:.1f} words)".format(avg_sentence_length))
    
    if avg_syllables_per_word > 1.5:
        suggestions.append("Use simpler words (current avg: {:.1f} syllables/word)".format(avg_syllables_per_word))
    
    if grade_level > target_grade:
        suggestions.append("Reduce complexity to reach grade {} level".format(target_grade))
    
    # Audience-specific suggestions
    if audience == "technical":
        suggestions.append("Consider adding technical glossary for complex terms")
    elif audience == "children":
        suggestions.append("Use more examples and simpler vocabulary")
    
    return {
        "text_length": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_sentence_length": round(avg_sentence_length, 1),
        "flesch_reading_ease": round(flesch_score, 1),
        "grade_level": round(grade_level, 1),
        "target_grade": target_grade,
        "audience": audience,
        "readability_assessment": "good" if flesch_score > 60 else "needs_improvement",
        "suggestions": suggestions
    }