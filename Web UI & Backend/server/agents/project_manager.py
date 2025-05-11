"""
Project Manager agent implementation
"""
from server.agents.huggingface_agent import HuggingFaceAgent
from server.config import PROJECT_MANAGER_ENDPOINT, HF_API_KEY
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

def get_project_manager_prompt(state: dict, config: RunnableConfig) -> list:
    """
    Define the system prompt for the project manager agent
    """
    system_prompt = """ Break down the given task into development, testing and documentation 
    """
    return [{"role": "system", "content": system_prompt}] + state["messages"]

def get_project_manager_agent(tools):
    """
    Create and return the project manager agent
    
    Args:
        tools: List of tools available to the agent
        
    Returns:
        The configured project manager agent
    """
    # Initialize the model
    model = HuggingFaceAgent(
        endpoint_url=PROJECT_MANAGER_ENDPOINT,
        api_key=HF_API_KEY,
        temperature=0.1,
        max_tokens=8192
    )
    
    # Create and return the agent
    return create_react_agent(
        model,
        tools,
        prompt=get_project_manager_prompt,
        name="project_manager",
    )
