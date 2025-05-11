"""
QA Tester agent implementation
"""
from server.agents.huggingface_agent import HuggingFaceAgent
from server.config import QA_TESTER_ENDPOINT, HF_API_KEY
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

def get_qa_tester_prompt(state: dict, config: RunnableConfig) -> list:
    """
    Define the system prompt for the QA tester agent
    """
    system_prompt = """Generate the testcases for the given code
    """
    return [{"role": "system", "content": system_prompt}] + state["messages"]

def get_qa_tester_agent(tools):
    """
    Create and return the QA tester agent
    
    Args:
        tools: List of tools available to the agent
        
    Returns:
        The configured QA tester agent
    """
    # Initialize the model
    model = HuggingFaceAgent(
        endpoint_url=QA_TESTER_ENDPOINT,
        api_key=HF_API_KEY,
        temperature=0.1,
        max_tokens=8192
    )
    
    # Create and return the agent
    return create_react_agent(
        model,
        tools,
        prompt=get_qa_tester_prompt,
        name="qa_tester",
    )
