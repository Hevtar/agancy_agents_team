"""
Prometheus metrics middleware for monitoring.
"""
import time
import prometheus_client
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Define metrics
REQUEST_COUNT = prometheus_client.Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = prometheus_client.Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

REQUESTS_IN_PROGRESS = prometheus_client.Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests currently in progress',
    ['method', 'endpoint']
)

TOKEN_USAGE = prometheus_client.Counter(
    'tokens_used_total',
    'Total tokens used',
    ['model', 'agent']
)

AGENT_EXECUTIONS = prometheus_client.Counter(
    'agent_executions_total',
    'Total agent executions',
    ['agent', 'status']
)

WORKFLOW_EXECUTIONS = prometheus_client.Counter(
    'workflow_executions_total',
    'Total workflow executions',
    ['workflow', 'status']
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and collect metrics."""
        method = request.method
        endpoint = request.url.path
        
        # Increment in-progress gauge
        REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
        
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
        # Decrement in-progress gauge
        REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()
        
        return response


def record_token_usage(model: str, agent: str, tokens: int):
    """Record token usage for a specific model and agent."""
    TOKEN_USAGE.labels(model=model, agent=agent).inc(tokens)


def record_agent_execution(agent: str, status: str):
    """Record agent execution."""
    AGENT_EXECUTIONS.labels(agent=agent, status=status).inc()


def record_workflow_execution(workflow: str, status: str):
    """Record workflow execution."""
    WORKFLOW_EXECUTIONS.labels(workflow=workflow, status=status).inc()