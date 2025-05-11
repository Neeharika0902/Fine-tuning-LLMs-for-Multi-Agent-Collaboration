import requests
import json
from langchain_core.language_models import BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, Dict, List, Mapping, Optional, Union
from server.config import HF_API_KEY

class HuggingFaceAgent(BaseLLM):
    """Custom LLM class for Hugging Face API with LangChain integration."""
    
    endpoint_url: str
    api_key: str = HF_API_KEY
    temperature: float = 0.1
    max_tokens: int = 8192
    
    def __init__(self, endpoint_url: str, **kwargs):
        """Initialize the HuggingFaceAgent."""
        super().__init__(**kwargs)
        self.endpoint_url = endpoint_url
        self.api_key = kwargs.get("api_key", HF_API_KEY)
        self.temperature = kwargs.get("temperature", 0.1)
        self.max_tokens = kwargs.get("max_tokens", 8192)
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Hugging Face API to generate text based on the prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "do_sample": True
            }
        }
        
        # Add any extra parameters from kwargs
        for key, value in kwargs.items():
            if key not in payload["parameters"]:
                payload["parameters"][key] = value
        
        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            
            # Extract and return the generated text
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return result.get("generated_text", "")
            
        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            return f"Error: {str(e)}"
    
    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "huggingface-api"
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Return identifying parameters."""
        return {
            "endpoint_url": self.endpoint_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
