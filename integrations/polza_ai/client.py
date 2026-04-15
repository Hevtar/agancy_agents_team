"""
Polza.Ai API Client with model routing and token management.
"""
import asyncio
import time
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager

import httpx
import yaml
from openai import AsyncOpenAI

from core.config import settings


class PolzaAIClient:
    """Client for interacting with Polza.Ai API using OpenAI SDK."""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.polza_ai_api_key
        self.base_url = base_url or settings.polza_ai_base_url
        
        # Initialize OpenAI client with Polza.Ai endpoint
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Load model routing configuration
        self.model_config = self._load_model_config()
        
        # Token tracking
        self.daily_token_usage = 0
        self.token_budget = settings.daily_token_budget
        
    def _load_model_config(self) -> Dict:
        """Load model routing configuration from YAML."""
        try:
            with open("integrations/polza_ai/model_routing.yaml", "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load model routing config: {e}")
            return {}
    
    async def check_token_budget(self, estimated_tokens: int) -> bool:
        """Check if we have enough tokens in the daily budget."""
        if self.daily_token_usage + estimated_tokens > self.token_budget:
            return False
        return True
    
    def get_model_for_agent(self, agent_name: str) -> tuple[str, str]:
        """Get the appropriate model for an agent based on routing config.
        
        Returns:
            tuple: (model_name, tier_name)
        """
        agent_mapping = self.model_config.get("agent_model_mapping", {})
        tier_name = agent_mapping.get(agent_name, 
                                      self.model_config.get("default_model_tier", "balanced"))
        
        tiers = self.model_config.get("model_tiers", {})
        tier_config = tiers.get(tier_name, {})
        
        model_name = tier_config.get("primary", "meta-llama/llama-3-70b-instruct")
        return model_name, tier_name
    
    async def create_completion(
        self,
        messages: list,
        agent_name: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False,
        **kwargs
    ) -> Any:
        """Create a completion using Polza.Ai API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            agent_name: Name of the agent (for model routing)
            model: Specific model to use (overrides routing)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            Completion response
        """
        # Determine model if not specified
        if not model and agent_name:
            model, tier = self.get_model_for_agent(agent_name)
        elif not model:
            model, tier = self.get_model_for_agent("default")
        
        # Get tier config for defaults
        tier_name = self._get_tier_for_model(model)
        tier_config = self.model_config.get("model_tiers", {}).get(tier_name, {})
        
        # Set defaults from tier config
        if temperature is None:
            temperature = tier_config.get("temperature", 0.4)
        if max_tokens is None:
            max_tokens = tier_config.get("max_tokens", 4096)
        
        # Create completion
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
            
            # Track token usage
            if not stream and hasattr(response, 'usage'):
                self.daily_token_usage += response.usage.total_tokens
            
            return response
            
        except Exception as e:
            print(f"Polza.Ai API error: {e}")
            raise
    
    def _get_tier_for_model(self, model: str) -> str:
        """Get the tier name for a given model."""
        for tier_name, tier_config in self.model_config.get("model_tiers", {}).items():
            if model in [tier_config.get("primary"), tier_config.get("fallback")]:
                return tier_name
        return "balanced"
    
    @asynccontextmanager
    async def streaming_completion(
        self,
        messages: list,
        agent_name: str = None,
        **kwargs
    ) -> AsyncGenerator:
        """Context manager for streaming completions."""
        stream = await self.create_completion(
            messages=messages,
            agent_name=agent_name,
            stream=True,
            **kwargs
        )
        try:
            yield stream
        finally:
            await stream.close()
    
    async def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text."""
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except:
            # Rough estimate: 4 characters per token
            return len(text) // 4
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "daily_token_usage": self.daily_token_usage,
            "token_budget": self.token_budget,
            "remaining_tokens": self.token_budget - self.daily_token_usage,
            "usage_percentage": (self.daily_token_usage / self.token_budget * 100) 
                               if self.token_budget > 0 else 0
        }
    
    async def reset_daily_usage(self):
        """Reset daily token usage (called at midnight)."""
        self.daily_token_usage = 0


# Singleton instance
_polza_client: Optional[PolzaAIClient] = None

def get_polza_client() -> PolzaAIClient:
    """Get or create the Polza.Ai client singleton."""
    global _polza_client
    if _polza_client is None:
        _polza_client = PolzaAIClient()
    return _polza_client