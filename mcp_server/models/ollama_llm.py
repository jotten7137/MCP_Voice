# mcp_server/models/ollama_llm.py
import logging
import json
import aiohttp
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger("mcp_server.ollama_llm")

class OllamaLLMService:
    """
    Language Model service that uses a local Ollama instance for generating responses.
    """
    
    def __init__(self, model_name: str = "llama2", ollama_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama LLM service.
        
        Args:
            model_name: Name of the model to use in Ollama
            ollama_url: URL of the Ollama API server
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        logger.info(f"Initialized Ollama LLM service with model: {model_name}")
    
    async def generate_response(self, message: str, 
                              session_id: str = None,
                              conversation: List[Dict[str, Any]] = None,
                              tool_results: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a response using the Ollama API.
        
        Args:
            message: User message
            session_id: Session ID
            conversation: Conversation history (if not provided, will use empty history)
            tool_results: Results from tool calls
            
        Returns:
            Dict with the generated response
        """
        try:
            # Prepare prompt with conversation context and tool results
            prompt = self._format_prompt(message, conversation, tool_results)
            
            # Call Ollama API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "max_tokens": 1024
                        }
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {error_text}")
                        raise Exception(f"Ollama API error: {response.status}")
                    
                    data = await response.json()
                    
                    # Extract the generated text
                    response_text = data.get("response", "")
                    
                    logger.info(f"Generated response: {response_text[:50]}...")
                    
                    # If conversation history provided, add this exchange
                    if conversation is None:
                        conversation = []
                    
                    # Add user message
                    conversation.append({
                        "role": "user",
                        "content": message
                    })
                    
                    # Add assistant message
                    conversation.append({
                        "role": "assistant",
                        "content": response_text
                    })
                    
                    return {
                        "message": response_text,
                        "conversation": conversation
                    }
                    
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "message": f"Error generating response: {str(e)}",
                "conversation": conversation or []
            }
    
    def _format_prompt(self, message: str, 
                     conversation: Optional[List[Dict[str, Any]]] = None,
                     tool_results: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Format the prompt for the Ollama API.
        
        Args:
            message: User message
            conversation: Conversation history
            tool_results: Results from tool calls
            
        Returns:
            Formatted prompt string
        """
        # Start with a system prompt
        prompt = "You are a helpful AI assistant that can assist with a wide range of tasks.\n\n"
        
        # Add conversation history
        if conversation:
            for msg in conversation:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "user":
                    prompt += f"User: {content}\n\n"
                elif role == "assistant":
                    prompt += f"Assistant: {content}\n\n"
        
        # Add tool results if provided
        if tool_results:
            prompt += "Tool Results:\n"
            for result in tool_results:
                tool_name = result.get("tool_name", "unknown")
                formatted = result.get("formatted", json.dumps(result.get("result", {}), indent=2))
                prompt += f"{tool_name} result:\n{formatted}\n\n"
        
        # Add the current message
        prompt += f"User: {message}\n\nAssistant:"
        
        return prompt