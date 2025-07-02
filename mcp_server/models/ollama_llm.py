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
                # Try using system message parameter for better instruction following
                system_message = """You are an AI assistant with tool access.

For weather questions: respond with @weather({"location": "CITY"})
For math questions: respond with @calculator({"expression": "MATH"})

No explanations needed, just the tool call."""
                
                # Simplified prompt for the user message
                user_prompt = self._format_user_prompt(message, conversation, tool_results)
                
                # Debug logging
                logger.info(f"System message: {system_message[:200]}...")
                logger.info(f"User prompt: {user_prompt[:200]}...")
                
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": user_prompt,
                        "system": system_message,
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
                    
                    logger.info(f"Full LLM response: {response_text}")
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
                        "conversation": conversation,
                        "raw_response": response_text  # Keep raw for tool extraction
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
        # Start with a system prompt that includes tool instructions
        prompt = """You are an AI assistant with access to tools. You MUST use tools when appropriate.

IMPORTANT: When users ask about weather or calculations, you MUST call the appropriate tool using this EXACT format:
@tool_name({"param": "value"})

Available tools:
- @calculator({"expression": "math expression"}) - REQUIRED for ANY math questions
- @weather({"location": "city name"}) - REQUIRED for ANY weather questions

EXAMPLES:
User: "What's the weather in London?"
You: "I'll check the weather for you. @weather({\"location\": \"London\"})"

User: "What's 15 + 25?"
You: "I'll calculate that. @calculator({\"expression\": \"15 + 25\"})"

You MUST use tools for weather and math. Do NOT give generic responses.

"""
        
        # Add conversation history
        if conversation:
            for msg in conversation:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "user":
                    prompt += f"User: {content}\n\n"
                elif role == "assistant":
                    prompt += f"Assistant: {content}\n\n"
        else:
            # Add few-shot examples if no conversation history
            prompt += """Here are examples of how to respond:

User: What's the weather in Paris?
Assistant: I'll check the weather for you. @weather({"location": "Paris"})

User: What's 10 + 15?
Assistant: I'll calculate that for you. @calculator({"expression": "10 + 15"})

User: How's the weather in Tokyo?
Assistant: Let me get the current weather. @weather({"location": "Tokyo"})

"""
        
        # Add tool results if provided
        if tool_results:
            prompt += "Tool Results:\n"
            for result in tool_results:
                tool_name = result.get("tool_name", "unknown")
                formatted = result.get("formatted", json.dumps(result.get("result", {}), indent=2))
                prompt += f"{tool_name} result:\n{formatted}\n\n"
        
        # Add the current message
        prompt += f"User: {message}\n\nAssistant:"
        
        # Debug: Log the prompt being sent
        logger.info(f"Sending prompt to Ollama: {prompt[:500]}...")
        
        return prompt
    
    def _format_user_prompt(self, message: str, 
                           conversation: Optional[List[Dict[str, Any]]] = None,
                           tool_results: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Format just the user prompt without system instructions (for use with system parameter).
        """
        prompt = ""
        
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