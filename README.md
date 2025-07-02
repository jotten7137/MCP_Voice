# MCP_Voice
MCP starter - voice and chat functionality with MCP boiler-plate potential

# Dependencies
## Ollama
Download: https://ollama.com/download
## Docker
Download: https://www.docker.com/products/docker-desktop/

## With Ollama:
ollama pull deepseek-coder:6.7b

## In Docker Terminal:
docker build -t mcp-voice .
docker run -d --name mcp-voice-new -p 8000:8000 mcp-voice

## In MCP_Voice project folder:
Open index.html

Use as a typical text and voice chat interface
Currently using qwq
