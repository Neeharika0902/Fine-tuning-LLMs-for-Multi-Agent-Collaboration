"""
Data Engineer agent implementation
"""
from server.agents.huggingface_agent import HuggingFaceAgent
from server.config import DATA_ENGINEER_ENDPOINT, HF_API_KEY, DATABASE_SCHEMA
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

def get_data_engineer_prompt(state: dict, config: RunnableConfig) -> list:
    """
    Define the system prompt for the data engineer agent
    """
    system_prompt = f"""Generate a Sql query based on user requirement: 
    """
    return [{"role": "system", "content": system_prompt}] + state["messages"]

def get_data_engineer_agent(tools):
    """
    Create and return the data engineer agent
    
    Args:
        tools: List of tools available to the agent
        
    Returns:
        The configured data engineer agent
    """
    # Initialize the model
    model = HuggingFaceAgent(
        endpoint_url=DATA_ENGINEER_ENDPOINT,
        api_key=HF_API_KEY,
        temperature=0.1,
        max_tokens=8192
    )
    
    # Create and return the agent
    return create_react_agent(
        model,
        tools,
        prompt=get_data_engineer_prompt,
        name="data_engineer",
    )
