"""
Deployment Engineer agent implementation
"""
from server.agents.huggingface_agent import HuggingFaceAgent
from server.config import DEPLOYMENT_ENGINEER_ENDPOINT, HF_API_KEY
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

def get_deployment_engineer_prompt(state: dict, config: RunnableConfig) -> list:
    """
    Define the system prompt for the deployment engineer agent
    """
    system_prompt = """ Generate the documentation for the given deployed code
    """
    return [{"role": "system", "content": system_prompt}] + state["messages"]

def get_deployment_engineer_agent(tools):
    """
    Create and return the deployment engineer agent
    
    Args:
        tools: List of tools available to the agent
        
    Returns:
        The configured deployment engineer agent
    """
    # Initialize the model
    model = HuggingFaceAgent(
        endpoint_url=DEPLOYMENT_ENGINEER_ENDPOINT,
        api_key=HF_API_KEY,
        temperature=0.1,
        max_tokens=8192
    )
    
    # Create and return the agent
    return create_react_agent(
        model,
        tools,
        prompt=get_deployment_engineer_prompt,
        name="deployment_engineer",
    )
