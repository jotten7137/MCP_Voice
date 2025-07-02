import os
from typing import Dict, Any, List

try:
    from pydantic_settings import BaseSettings
    
    class Settings(BaseSettings):
        model_config = {"extra": "ignore", "env_file": ".env", "env_prefix": "MCP_", "case_sensitive": False}
        
        # Server settings
        HOST: str = "0.0.0.0"
        PORT: int = 8000
        DEBUG: bool = True
        
        # Authentication
        AUTH_REQUIRED: bool = False
        API_KEY_SECRET: str = "your-secret-key-change-me"  # Change in production!
        
        # Paths
        CACHE_DIR: str = "./cache"
        MODEL_DIR: str = "./models"

        # Model settings
        STT_MODEL: str = "openai/whisper-base"  # Options: small, medium, large
        #LLM_MODEL: str = "meta-llama/Llama-2-7b-chat-hf"  # Use a Hugging Face model ID
        OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
        LLM_MODEL: str = os.getenv("LLM_MODEL", "qwq:32b")
        TTS_MODEL_DIR: str = os.path.join("./models", "tts")
        TTS_MODEL: str = os.getenv("TTS_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
        
        # Processing settings
        MAX_AUDIO_LENGTH_SECONDS: int = 60
        MAX_TOKENS: int = 1024
        TEMPERATURE: float = 0.7
        TOP_P: float = 0.9
        
        # Feature flags
        GENERATE_AUDIO_RESPONSE: bool = True
        ALLOW_TOOL_CALLS: bool = True
        
        # Tool settings
        ENABLED_TOOLS: list = ["weather", "calculator"]
        
        # Individual tool configs (loaded from env)
        WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "a32388aba00ba920e2abf48418dc2995")
        WEATHER_DEFAULT_LOCATION: str = "San Francisco"
        
        @property
        def TOOL_CONFIGS(self) -> Dict[str, Dict[str, Any]]:
            return {
                "weather": {
                    "api_key": self.WEATHER_API_KEY,
                    "default_location": self.WEATHER_DEFAULT_LOCATION
                },
                "calculator": {}
            }
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings
    
    class Settings(BaseSettings):
        # Server settings
        HOST: str = "0.0.0.0"
        PORT: int = 8000
        DEBUG: bool = True
        
        # Authentication
        AUTH_REQUIRED: bool = False
        API_KEY_SECRET: str = "your-secret-key-change-me"  # Change in production!
        
        # Paths
        CACHE_DIR: str = "./cache"
        MODEL_DIR: str = "./models"

        # Model settings
        STT_MODEL: str = "openai/whisper-base"  # Options: small, medium, large
        #LLM_MODEL: str = "meta-llama/Llama-2-7b-chat-hf"  # Use a Hugging Face model ID
        OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
        LLM_MODEL: str = os.getenv("LLM_MODEL", "qwq:32b")
        TTS_MODEL_DIR: str = os.path.join(MODEL_DIR, "tts")
        TTS_MODEL: str = os.getenv("TTS_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
        
        # Processing settings
        MAX_AUDIO_LENGTH_SECONDS: int = 60
        MAX_TOKENS: int = 1024
        TEMPERATURE: float = 0.7
        TOP_P: float = 0.9
        
        # Feature flags
        GENERATE_AUDIO_RESPONSE: bool = True
        ALLOW_TOOL_CALLS: bool = True
        
        # Tool settings
        ENABLED_TOOLS: List[str] = ["weather", "calculator"]
        TOOL_CONFIGS: Dict[str, Dict[str, Any]] = {
            "weather": {
                "api_key": os.getenv("WEATHER_API_KEY", "a32388aba00ba920e2abf48418dc2995"),
                "default_location": "San Francisco"
            },
            "calculator": {}
        }
        
        class Config:
            env_file = ".env"
            env_prefix = "MCP_"

# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.CACHE_DIR, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
