"""
Project Manager Agent - Coordinates workflows and manages task delegation.
"""
from typing import Dict, List, Optional, Any
from core.base_agent import BaseAgent, AgentMemory, AgentState


class ProjectManagerAgent(BaseAgent):
    """
    Project Manager Agent responsible for:
    - Coordinating workflows between agents
    - Managing task delegation and priorities
    - Tracking project progress
    - Handling escalations and blockers
    """
    
    def __init__(self, memory: Optional[AgentMemory] = None, **kwargs):
        system_prompt = """You are an experienced Project Manager in a digital marketing agency.
Your role is to coordinate workflows, manage task delegation, and ensure projects are delivered on time.

Key responsibilities:
1. Break down complex projects into manageable tasks
2. Assign tasks to appropriate agents based on their expertise
3. Monitor progress and adjust priorities as needed
4. Identify and resolve blockers
5. Communicate status updates to stakeholders

You are organized, detail-oriented, and excellent at prioritization.
You always consider dependencies between tasks and optimize for efficiency.

When analyzing a project:
- First understand the overall goals and constraints
- Identify required skills and resources
- Create a logical sequence of tasks
- Assign tasks to the most suitable agents
- Set up checkpoints for progress review

Always maintain a professional and solution-oriented approach."""
        
        super().__init__(
            name="project_manager",
            role="Project Manager",
            goal="Coordinate marketing projects and ensure successful delivery",
            system_prompt=system_prompt,
            allow_delegation=True,
            memory=memory,
            **kwargs
        )
    
    async def create_project_plan(self, project_description: str, constraints: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a detailed project plan from a description."""
        prompt = f"""Analyze this marketing project and create a detailed plan:

Project: {project_description}

Constraints: {constraints or 'None specified'}

Please provide:
1. Project objectives and success criteria
2. Required tasks with dependencies
3. Recommended agent assignments for each task
4. Estimated timeline
5. Key milestones and checkpoints
6. Potential risks and mitigation strategies

Format the response as a structured project plan."""
        
        return await self.execute(prompt)
    
    async def assign_tasks(self, tasks: List[Dict], available_agents: List[str]) -> Dict[str, str]:
        """Assign tasks to agents based on their expertise."""
        prompt = f"""Assign these tasks to the most suitable agents:

Tasks: {tasks}
Available agents: {available_agents}

Consider each agent's expertise and current workload.
Provide a mapping of task_id to agent_name with justification."""
        
        return await self.execute(prompt)
    
    async def assess_progress(self, completed_tasks: List[Dict], pending_tasks: List[Dict], blockers: List[str]) -> Dict[str, Any]:
        """Assess project progress and identify issues."""
        prompt = f"""Assess the current project status:

Completed tasks: {completed_tasks}
Pending tasks: {pending_tasks}
Current blockers: {blockers}

Provide:
1. Overall progress percentage
2. Tasks at risk
3. Recommended actions to address blockers
4. Adjusted timeline if needed
5. Resource reallocation suggestions"""
        
        return await self.execute(prompt)


# Singleton instance
_project_manager_instance = None

def get_project_manager_agent(memory: Optional[AgentMemory] = None, **kwargs) -> ProjectManagerAgent:
    """Get or create the Project Manager agent instance."""
    global _project_manager_instance
    if _project_manager_instance is None:
        _project_manager_instance = ProjectManagerAgent(memory=memory, **kwargs)
    return _project_manager_instance